import sqlite3
import json
import hashlib
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional, List
import logging

logger = logging.getLogger(__name__)

class TaskCache:
    """Cache for storing complete task execution results"""
    
    def __init__(self, cache_dir="cache"):
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(exist_ok=True)
        self.db_path = self.cache_dir / "task_cache.db"
        self._init_db()
    
    def _init_db(self):
        """Initialize the database schema for complete task results"""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute('''
                CREATE TABLE IF NOT EXISTS task_results (
                    task_id TEXT NOT NULL,
                    server_name TEXT,
                    model_name TEXT NOT NULL,
                    task_description TEXT,
                    status TEXT,
                    
                    -- Timing metrics
                    execution_time REAL,
                    agent_execution_time REAL,
                    evaluation_time REAL,
                    
                    -- Execution details (stored as JSON)
                    execution_results TEXT,  -- JSON array of execution steps
                    final_solution TEXT,
                    total_rounds INTEGER,
                    evaluation TEXT,  -- JSON object with all evaluation metrics
                    
                    -- Token usage
                    total_output_tokens INTEGER,
                    total_prompt_tokens INTEGER,
                    total_tokens INTEGER,
                    
                    -- Metadata
                    timestamp TEXT NOT NULL,
                    
                    PRIMARY KEY (task_id, model_name, server_name)
                )
            ''')
            
            # Create indexes for faster lookups
            conn.execute('''
                CREATE INDEX IF NOT EXISTS idx_task_model_server 
                ON task_results(task_id, model_name, server_name)
            ''')
            conn.execute('''
                CREATE INDEX IF NOT EXISTS idx_model_status 
                ON task_results(model_name, status)
            ''')
            conn.execute('''
                CREATE INDEX IF NOT EXISTS idx_timestamp 
                ON task_results(timestamp)
            ''')
    
    def get_cached_result(self, task_id: str, model_name: str, server_name: str = None) -> Optional[Dict[str, Any]]:
        """Retrieve cached result for a specific task"""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            if server_name is None:
                result = conn.execute(
                    "SELECT * FROM task_results WHERE task_id = ? AND model_name = ? AND (server_name IS NULL OR server_name = '')",
                    (task_id, model_name)
                ).fetchone()
            else:
                result = conn.execute(
                    "SELECT * FROM task_results WHERE task_id = ? AND model_name = ? AND server_name = ?",
                    (task_id, model_name, server_name)
                ).fetchone()

        if result:
            cached_data = dict(result)
            
            # Reconstruct the complete result object
            reconstructed_result = {
                'task_id': cached_data['task_id'],
                'server_name': cached_data['server_name'],
                'model_name': cached_data['model_name'],
                'task_description': cached_data['task_description'],
                'status': cached_data['status'],
                'execution_time': cached_data['execution_time'],
                'agent_execution_time': cached_data['agent_execution_time'],
                'evaluation_time': cached_data['evaluation_time'],
                'execution_results': json.loads(cached_data['execution_results']) if cached_data['execution_results'] else [],
                'final_solution': cached_data['final_solution'],
                'total_rounds': cached_data['total_rounds'],
                'evaluation': json.loads(cached_data['evaluation']) if cached_data['evaluation'] else {},
                'total_output_tokens': cached_data['total_output_tokens'],
                'total_prompt_tokens': cached_data['total_prompt_tokens'],
                'total_tokens': cached_data['total_tokens'],
                'cached_timestamp': cached_data['timestamp'],
                'from_cache': True
            }
            
            logger.info(f"Retrieved cached result for task {task_id} with model {model_name}")
            return reconstructed_result
        
        return None
        
    def get_cached_task_in_range(self, range_start: int, model_name: str, server_name: str = None) -> Optional[str]:
        """Get the task_id of a cached task in the specified range (e.g., 0-9, 10-19)"""
        
        with sqlite3.connect(self.db_path) as conn:
            if server_name is None:
                result = conn.execute('''
                    SELECT task_id FROM task_results 
                    WHERE model_name = ? 
                    AND (server_name IS NULL OR server_name = '')
                    AND CAST(substr(task_id, length(task_id) - 2) AS INTEGER) / 10 = ?
                    LIMIT 1
                ''', (model_name, range_start // 10)).fetchone()
            else:
                result = conn.execute('''
                    SELECT task_id FROM task_results 
                    WHERE model_name = ? AND server_name = ?
                    AND CAST(substr(task_id, length(task_id) - 2) AS INTEGER) / 10 = ?
                    LIMIT 1
                ''', (model_name, server_name, range_start // 10)).fetchone()
        
        return result[0] if result else None

    def cache_result(self, task_id: str, model_name: str, result: Dict[str, Any]) -> None:
        """
        Cache a complete task result
        
        Args:
            task_id: Unique task identifier
            model_name: Name of the model used
            result: Complete result dictionary containing all task execution data
        """
        server_name = result.get('server_name', '')
        timestamp = datetime.now().isoformat()
        
        # Safely extract values from result with defaults
        def safe_get(key: str, default=None):
            return result.get(key, default)
        
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.execute('''
                    INSERT OR REPLACE INTO task_results (
                        task_id, server_name, model_name, task_description, status,
                        execution_time, agent_execution_time, evaluation_time,
                        execution_results, final_solution, total_rounds, evaluation,
                        total_output_tokens, total_prompt_tokens, total_tokens,
                        timestamp
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    task_id,
                    server_name,
                    model_name,
                    safe_get('task_description'),
                    safe_get('status', 'unknown'),
                    safe_get('execution_time'),
                    safe_get('agent_execution_time'),
                    safe_get('evaluation_time'),
                    json.dumps(safe_get('execution_results', []), ensure_ascii=False),
                    safe_get('final_solution', ''),
                    safe_get('total_rounds', 0),
                    json.dumps(safe_get('evaluation', {}), ensure_ascii=False),
                    safe_get('total_output_tokens', 0),
                    safe_get('total_prompt_tokens', 0),
                    safe_get('total_tokens', 0),
                    timestamp
                ))
            
            logger.info(f"Cached result for task {task_id} with model {model_name}")
            
        except Exception as e:
            logger.error(f"Failed to cache result for task {task_id}: {e}")
    
    def has_cached_result(self, task_id: str, model_name: str, server_name: str = None) -> bool:
        """Check if a result is already cached without retrieving it"""
        with sqlite3.connect(self.db_path) as conn:
            if server_name is None:
                result = conn.execute(
                    "SELECT 1 FROM task_results WHERE task_id = ? AND model_name = ? AND (server_name IS NULL OR server_name = '')",
                    (task_id, model_name)
                ).fetchone()
            else:
                result = conn.execute(
                    "SELECT 1 FROM task_results WHERE task_id = ? AND model_name = ? AND server_name = ?",
                    (task_id, model_name, server_name)
                ).fetchone()
        
        return result is not None
    
    def get_model_summary(self, model_name: str, server_name: str = None) -> Dict[str, Any]:
        """Get summary statistics for a specific model"""
        query = "SELECT * FROM task_results WHERE model_name = ?"
        params = [model_name]
        
        if server_name:
            query += " AND server_name = ?"
            params.append(server_name)
        
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            results = conn.execute(query, params).fetchall()
        
        if not results:
            return {"total_cached_tasks": 0}
        
        # Calculate summary statistics
        total_tasks = len(results)
        completed_tasks = len([r for r in results if r['status'] == 'completed'])
        
        # Average timing metrics (only for completed tasks)
        completed = [r for r in results if r['status'] == 'completed']
        
        summary = {
            "total_cached_tasks": total_tasks,
            "completed_tasks": completed_tasks,
            "completion_rate": completed_tasks / total_tasks if total_tasks > 0 else 0
        }
        
        if completed:
            summary.update({
                "avg_execution_time": sum(r['execution_time'] or 0 for r in completed) / len(completed),
                "avg_agent_execution_time": sum(r['agent_execution_time'] or 0 for r in completed) / len(completed),
                "avg_evaluation_time": sum(r['evaluation_time'] or 0 for r in completed) / len(completed),
                "avg_total_rounds": sum(r['total_rounds'] or 0 for r in completed) / len(completed),
                "avg_total_tokens": sum(r['total_tokens'] or 0 for r in completed) / len(completed),
                "avg_output_tokens": sum(r['total_output_tokens'] or 0 for r in completed) / len(completed),
                "avg_prompt_tokens": sum(r['total_prompt_tokens'] or 0 for r in completed) / len(completed)
            })
        
        return summary
    
    def get_cached_tasks_by_model(self, model_name: str) -> List[Dict[str, Any]]:
        """Get all cached tasks for a specific model"""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            results = conn.execute(
                "SELECT task_id, server_name, status, execution_time, timestamp FROM task_results WHERE model_name = ? ORDER BY timestamp DESC",
                (model_name,)
            ).fetchall()
        
        return [dict(row) for row in results]
    
    def clear_cache(self, task_id: str = None, model_name: str = None, server_name: str = None) -> int:
        """Clear cache entries based on filters. Returns number of deleted entries."""
        conditions = []
        params = []
        
        if task_id:
            conditions.append("task_id = ?")
            params.append(task_id)
        if model_name:
            conditions.append("model_name = ?")
            params.append(model_name)
        if server_name:
            conditions.append("server_name = ?")
            params.append(server_name)
        
        if conditions:
            query = f"DELETE FROM task_results WHERE {' AND '.join(conditions)}"
        else:
            query = "DELETE FROM task_results"
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute(query, params)
            rows_affected = cursor.rowcount
        
        logger.info(f"Cleared {rows_affected} cached results")
        return rows_affected
    
    def list_cached_tasks(self, limit: int = None) -> List[Dict[str, Any]]:
        """List all cached tasks with basic info"""
        query = '''
            SELECT task_id, server_name, model_name, status, execution_time, 
                   agent_execution_time, total_tokens, timestamp
            FROM task_results 
            ORDER BY timestamp DESC
        '''
        
        params = []
        if limit:
            query += " LIMIT ?"
            params.append(limit)
        
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            results = conn.execute(query, params).fetchall()
        
        return [dict(row) for row in results]
    
    def get_cache_stats(self) -> Dict[str, Any]:
        """Get overall cache statistics"""
        with sqlite3.connect(self.db_path) as conn:
            stats = conn.execute('''
                SELECT 
                    COUNT(*) as total_tasks,
                    COUNT(DISTINCT model_name) as unique_models,
                    COUNT(DISTINCT server_name) as unique_servers,
                    COUNT(CASE WHEN status = 'completed' THEN 1 END) as completed_tasks,
                    AVG(CASE WHEN status = 'completed' THEN execution_time END) as avg_execution_time,
                    SUM(total_tokens) as total_tokens_used
                FROM task_results
            ''').fetchone()
        
        return {
            "total_cached_tasks": stats[0],
            "unique_models": stats[1],
            "unique_servers": stats[2],
            "completed_tasks": stats[3],
            "completion_rate": (stats[3] / stats[0]) if stats[0] > 0 else 0,
            "avg_execution_time": stats[4],
            "total_tokens_used": stats[5] or 0
        }