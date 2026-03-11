"""Test server C for UK Power Networks electricity demand and generation queries."""
from mcp.server.fastmcp import FastMCP
from mcp_servers.test_servers.api_manager import make_request_uk_powernetworks
from dotenv import load_dotenv
from datetime import datetime

# Initialize FastMCP server
load_dotenv()
mcp = FastMCP("server_C_test", debug=True)


## Standard Profiles UK Power Networks Uses for Electricity Demand

@mcp.tool()
async def electricity_demand_timestamps_for_domestic_above(domestic: float) -> str:
    """    
    Fetches the timestamps for measurements of Standard Profiles UK Power Networks 
    Uses for Electricity Demand that are above the given domestic electricity demand. 
    List in descending order and limited to 5 results.

    Args:
        domestic (float): The domestic electricity demand in %.

    Returns:
        timestamp (str): The time stamp of the measurements.
        domestic (str): The domestic electricity demand in %.
    """

    params = {
        "select": "timestamp, domestic",
        "where": f"domestic > {domestic}",
        "ORDER_BY": "timestamp DESC",
        "LIMIT": "5",
    }
    return await make_request_uk_powernetworks("ukpn-standard-profiles-electricity-demand", params)



@mcp.tool()
async def electricity_demand_storage_for_timestamp(timestamp: datetime) -> str:
    """    
    Fetches the latest storage for a measurements of Standard Profiles UK Power Networks 
    Uses for Electricity Demand made up to and including the date. If no time is given,
    the latest storage for that date is returned. List in descending order and limited to 5 results.

    Args:
        timestamp (datetime): The date and time the measurement was done. If no time is given, the full day of the specified date is expected 'YYYY-MM-DDT23:59:00+00:0'.

    Returns:
        storage (str): The energy storage in percent of the measurement.
        timestamp (str): The time stamp of the measurement.
        
    """

    params = {
        "select": "storage, timestamp ",
        "where": f"timestamp <= '{timestamp}' ",
        "order_by": "timestamp DESC ",
        "LIMIT": "5",
    }
    return await make_request_uk_powernetworks("ukpn-standard-profiles-electricity-demand", params)



## Standard Profiles UK Power Networks Uses for Electricity Generation

@mcp.tool()
async def electricity_generation_timestamps_for_wind_above(wind: float) -> str:
    """    
    Fetches the timestamps for measurements of Standard Profiles UK Power Networks 
    Uses for Electricity Generation that are above the given wind electricity generation. 
    List in descending order and limited to 5 results.

    Args:
        wind (float): The wind electricity demand in %.

    Returns:
        timestamp (str): The time stamp of the measurements.
        wind (str): The wind electricity generation in %.
    """

    params = {
        "select": "timestamp, wind",
        "where": f"wind > {wind}",
        "order_by": "timestamp DESC ",
        "LIMIT": "5"
    }
    return await make_request_uk_powernetworks("ukpn-standard-technology-profiles-generation", params)



@mcp.tool()
async def electricity_generation_storage_for_timestamp(timestamp: datetime) -> str:
    """    
    Fetches the lastest storage for a measurements of Standard Profiles UK Power Networks 
    Uses for Electricity Generation which was made up to and including the date timestamp. If no time is given,
    the latest storage for that date is returned. 
    List in descending order and limited to 5 results.

    Args:
        timestamp (datetime): The date that the measurement was done. If no time is given, the full day of the specified date is expected 'YYYY-MM-DDT23:59:00+00:0'.

    Returns:
        storage (str): The energy storage in percent of the measurement.
        timestamp (str): The time stamp of the measurement.
    """

    params = {
        "select": "storage, timestamp ",
        "where": f"timestamp <= '{timestamp}' ",
        "order_by": "timestamp DESC ",
        "LIMIT": "5",
    }
    return await make_request_uk_powernetworks("ukpn-standard-technology-profiles-generation", params)


## Live faults

@mcp.tool()
async def live_faults_creationdate_for_reference(incidentreference: str) -> str:
    """    
    Fetches the creation date for a measurements of Live Faults with an incidentreference.

    Args:
        incidentreference (str): The refenrece number of the incident that the measurement was done.

    Returns:
        creationdatetime (str): The date and time of the measurement.
        incidentreference may have multiple measurements. creationdatetime may appear on multiple rows.
    """

    params = {
        "select": "creationdatetime",
        "where": f"incidentreference = '{incidentreference}' ",
        "limit": "1",
    }
    return await make_request_uk_powernetworks("ukpn-live-faults", params)



@mcp.tool()
async def live_faults_reference_for_postcode(postcodesaffected : str) -> str:
    """    
    Fetches the incident reference for a measurements of Live Faults using the post codes affected by the incident.

    Args:
        postcodesaffected (str): The post code that were affected of the incident.

    Returns:
        incidentreference (str): The refenrece number of the incident that the measurement was done.
    """

    params = {
        "select": "incidentreference",
        "where": f"postcodesaffected = '{postcodesaffected}'",
    }
    return await make_request_uk_powernetworks("ukpn-live-faults", params)


@mcp.tool()
async def live_faults_priority_for_reference(incidentreference: str) -> str:
    """    
    Fetches the priority of an incident for a measurements of Live Faults with an incidentreference.

    Args:
        incidentreference (str): The refenrece number of the incident that the measurement was done.

    Returns:
        incidentpriority (str): The priority of the incident of the measurement. 1 is highest priority.
        incidentreference may have multiple measurements. incidentpriority may appear on multiple rows.
    """

    params = {
        "select": "incidentpriority",
        "where": f"incidentreference = '{incidentreference}' ",
        "limit": "1",
    }
    return await make_request_uk_powernetworks("ukpn-live-faults", params)


@mcp.tool()
async def live_faults_message_for_reference(incidentreference: str) -> str:
    """    
    Fetches the main message of an incident for a measurements of Live Faults with an incidentreference.

    Args:
        incidentreference (str): The refenrece number of the incident that the measurement was done.

    Returns:
        mainmessage (str): The main message of the incident of the measurement.
        incidentreference may have multiple measurements. main message may appear on multiple rows.
    """

    params = {
        "select": "mainmessage ",
        "where": f"incidentreference = '{incidentreference}'",
    }
    return await make_request_uk_powernetworks("ukpn-live-faults", params)


@mcp.tool()
async def live_faults_powercuttype_for_reference(incidentreference: str) -> str:
    """    
    Fetches the power cut type of an incident for a measurements of Live Faults with an incidentreference.

    Args:
        incidentreference (str): The refenrece number of the incident that the measurement was done.

    Returns:
        powercuttype (str): The type of power cut of the incident. 
        incidentreference may have multiple measurements. Power cut type may appear on multiple rows.
        Power cut types: "Planned", "Unplanned", "Restored"
    """

    params = {
        "select": "powercuttype",
        "where": f"incidentreference = '{incidentreference}' ",
        "limit": "1",
    }
    return await make_request_uk_powernetworks("ukpn-live-faults", params)

@mcp.tool()
async def live_faults_description_for_reference(incidentreference: str) -> str:
    """    
    Fetches the description of an incident for a measurements of Live Faults with an incidentreference.

    Args:
        incidentreference (str): The refenrece number of the incident that the measurement was done.

    Returns:
        incidentcategorycustomerfriendlydescription (str): A customer friendly description of 
         an incident. incidentreference may have multiple measurements. 
          incidentcategorycustomerfriendlydescription may appear on multiple rows.
    """

    params = {
        "select": "incidentcategorycustomerfriendlydescription",
        "where": f"incidentreference = '{incidentreference}'",
    }
    return await make_request_uk_powernetworks("ukpn-live-faults", params)


@mcp.tool()
async def live_faults_count_for_reference(incidentreference: str) -> str:
    """    
    Fetches the incident count for a measurements of Live Faults with an incidentreference.

    Args:
        incidentreference (str): The refenrece number of the incident that the measurement was done.

    Returns:
        incidentscount (str): A count of incidents of 
         an incident. incidentreference may have multiple measurements. 
          incidentscount may appear on multiple rows.
    """
    params = {
        "select": "incidentscount ",
        "where": f"incidentreference = '{incidentreference}'",
    }
    return await make_request_uk_powernetworks("ukpn-live-faults", params)


if __name__ == "__main__":
    mcp.run(transport='stdio')