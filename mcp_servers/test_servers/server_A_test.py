"""Test server A for UK Power Networks metadata queries."""

from mcp.server.fastmcp import FastMCP
from mcp_servers.test_servers.api_manager import make_request_uk_powernetworks
from dotenv import load_dotenv

# Initialize FastMCP server
load_dotenv()
mcp = FastMCP("server_B_test", debug=True)


### Namngivning av tools kanske kan ändras
    ### alla i server a test kommer från metadata och alla tar in identifier

@mcp.tool()
async def metadata_creator_for_identifier(identifier: str) -> str:
    """    
    Fetches the creator of metadatafor a specified identifier.

    Args:
        identifier (str): The identifier of the metadata.

    Returns:
        dublin_core_creator (str): The owner of the metadata.

    """

    params = {
        "select": "dublin_core_creator",
        "where": f"identifier = '{identifier}'",
    }

    return await make_request_uk_powernetworks("domain-dataset0", params)


@mcp.tool()
async def metadata_description_for_identifier(identifier: str) -> str:
    """    
    Fetches the description as a HTML and makes it readable of metadata for a specified identifier.

    Args:
        identifier (str): The identifier of the metadata.

    Returns:
        dublin_core_description (str): The description of the metadata.
    """

    params = {
        "select": "dublin_core_description",
        "where": f"identifier = '{identifier}'",
    }

    return await make_request_uk_powernetworks("domain-dataset0", params)


@mcp.tool()
async def metadata_subject_for_identifier(identifier: str) -> str:
    """    
    Fetches the subject of metadata for a specified identifier.

    Args:
        identifier (str): The identifier of the metadata.

    Returns:
        dublin_core_subject (str): The subject of the metadata.
    """

    params = {
        "select": "dublin_core_subject",
        "where": f"identifier = '{identifier}'",
    }

    return await make_request_uk_powernetworks("domain-dataset0", params)


@mcp.tool()
async def metadata_type_for_identifier(identifier: str) -> str:
    """    
    Fetches the type of metadata for a specified identifier.

    Args:
        identifier (str): The identifier of the metadata.

    Returns:
        dublin_core_type (str): The subject of the metadata.
    """

    params = {
        "select": "dublin_core_type",
        "where": f"identifier = '{identifier}'",
    }

    return await make_request_uk_powernetworks("domain-dataset0", params)


@mcp.tool()
async def metadata_date_issued_for_identifier(identifier: str) -> str:
    """    
    Fetches the date of issue of metadata for a specified identifier.

    Args:
        identifier (str): The identifier of the metadata.

    Returns:
        dublin_core_issued (str): The date issued of the metadata.
    """

    params = {
        "select": "dublin_core_issued",
        "where": f"identifier = '{identifier}'",
    }

    return await make_request_uk_powernetworks("domain-dataset0", params)

@mcp.tool()
async def metadata_date_modified_for_identifier(identifier: str) -> str:
    """    
    Fetches the date of modification of metadata for a specified identifier.

    Args:
        identifier (str): The identifier of the metadata.

    Returns:
        dublin_core_modified (str): The date modified of the metadata.
    """

    params = {
        "select": "dublin_core_modified",
        "where": f"identifier = '{identifier}'",
    }

    return await make_request_uk_powernetworks("domain-dataset0", params)


@mcp.tool()
async def metadata_access_rights_for_identifier(identifier: str) -> str:
    """    
    Fetches the access rights of metadata for a specified identifier.

    Args:
        identifier (str): The identifier of the metadata.

    Returns:
        dublin_core_accessrights (str): The access rights of the metadata.
    """

    params = {
        "select": "dublin_core_accessrights",
        "where": f"identifier = '{identifier}'",
    }

    return await make_request_uk_powernetworks("domain-dataset0", params)

@mcp.tool()
async def metadata_identifier_for_title(dublin_core_title: str) -> str:
    """    
    Fetches the identifier of metadata for a specified title.

    Args:
        dublin_core_title (str): The title of the metadata.

    Returns:
        identifier (str): The identifier of the metadata.
    """

    params = {
        "select": "identifier",
        "where": f"dublin_core_title = '{dublin_core_title}'",
    }

    return await make_request_uk_powernetworks("domain-dataset0", params)


@mcp.tool()
async def metadata_format_for_identifier(identifier: str) -> str:
    """    
    Fetches the format of metadata for a specified identifier.

    Args:
        identifier (str): The identifier of the metadata.

    Returns:
        dublin_core_format (str): The format of the metadata.
    """

    params = {
        "select": "dublin_core_format",
        "where": f"identifier = '{identifier}'",
    }

    return await make_request_uk_powernetworks("domain-dataset0", params)


@mcp.tool()
async def metadata_relation_for_identifier(identifier: str) -> str:
    """    
    Fetches the relation of metadata for a specified identifier.

    Args:
        identifier (str): The identifier of the metadata.

    Returns:
        dublin_core_relation (str): The relation of the metadata.
    """

    params = {
        "select": "dublin_core_relation",
        "where": f"identifier = '{identifier}'",
    }

    return await make_request_uk_powernetworks("domain-dataset0", params)


@mcp.tool()
async def metadata_source_for_identifier(identifier: str) -> str:
    """    
    Fetches the source of metadata for a specified identifier.

    Args:
        identifier (str): The identifier of the metadata.

    Returns:
        dublin_core_source (str): The source of the metadata.
    """

    params = {
        "select": "dublin_core_source",
        "where": f"identifier = '{identifier}'",
    }

    return await make_request_uk_powernetworks("domain-dataset0", params)


@mcp.tool()
async def metadata_publisher_for_identifier(identifier: str) -> str:
    """    
    Fetches the publisher of metadata for a specified identifier.

    Args:
        identifier (str): The identifier of the metadata.

    Returns:
        dublin_core_publisher (str): The publisher of the metadata.
    """

    params = {
        "select": "dublin_core_publisher",
        "where": f"identifier = '{identifier}'",
    }

    return await make_request_uk_powernetworks("domain-dataset0", params)


@mcp.tool()
async def metadata_visibility_for_identifier(identifier: str) -> str:
    """    
    Fetches the visibility of metadata for a specified identifier.

    Args:
        identifier (str): The identifier of the metadata.

    Returns:
        visibility (str): The visibility of the metadata (domain or restricted).
    """

    params = {
        "select": "visibility",
        "where": f"identifier = '{identifier}'",
    }

    return await make_request_uk_powernetworks("domain-dataset0", params)

@mcp.tool()
async def metadata_published_for_identifier(identifier: str) -> str:
    """    
    Fetches if it is published, of metadata for a specified identifier.

    Args:
        identifier (str): The identifier of the metadata.

    Returns:
        publishing_published (str): If something is published or not (true or false).
    """

    params = {
        "select": "publishing_published",
        "where": f"identifier = '{identifier}'",
    }

    return await make_request_uk_powernetworks("domain-dataset0", params)



if __name__ == "__main__":
    mcp.run(transport='stdio')
