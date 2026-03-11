"""Test server B for UK Power Networks regional power and substation queries."""

from mcp.server.fastmcp import FastMCP
from mcp_servers.test_servers.api_manager import make_request_uk_powernetworks
from dotenv import load_dotenv

# Initialize FastMCP server
load_dotenv()
mcp = FastMCP("server_B_test", debug=True)

# dataset - Regional Power sites

@mcp.tool()
async def regional_power_site_names_before_year(year: str) -> str:
    """
    Return a list of site names for sites assessed before a given year. Dates are stored in
    the format 'year-month-day', example '2001-01-20'.

    Args:
        year (str): The year (in 'YYYY' format) to filter sites assessment date.

    Returns:
        sitename (str): A site name from the OpenDataSoft API.
    """
    params = {
        "select": "sitename",
        "where": f"assessmentdate < '{year}' ",
        "order_by": "assessmentdate DESC ",
        "limit": 5
    }
    return await make_request_uk_powernetworks("grid-and-primary-sites", params)

@mcp.tool()
async def regional_power_resistance_before_year(year: str) -> str:
    """
    Return a list of measured resistances for sites assesed before a given year. Dates are stored in
    the format 'year-month-day', example '2001-01-20'.

    Args:
        year (str): The year (in 'YYYY' format) to filter sites assesed before.

    Returns:
        measuredresistance_ohm (str): The resistances from the OpenDataSoft API.
    """
    params = {
        "select": "measuredresistance_ohm",
        "where": f"assessmentdate < '{year}' AND measuredresistance_ohm IS NOT NULL ",
        "order_by": "assessmentdate DESC ",
        "limit": 5
    }
    return await make_request_uk_powernetworks("grid-and-primary-sites", params)

@mcp.tool()
async def regional_power_sites_voltage_for_sitename(sitename: str) -> str:
    """
    Fetches the regional power site voltage level of UK Power Networks for a specified sitename.
    
    Args:
        sitename (str): The name of the site.

    Returns:
        sitevoltage (str): The voltage levels as a string.
    
    """
    params = {
        "select": "sitevoltage",
        "where": f"sitename = '{sitename}'",
    }
    return await make_request_uk_powernetworks("grid-and-primary-sites", params)


@mcp.tool()
async def regional_power_sites_licence_area_for_sitename(sitename: str) -> str:
    """
    Fetches the regional power licence area of UK Power Networks for a specified sitename.
    
    Args:
        sitename (str): The name of the site.

    Returns:
        licencearea (str): The licence area as a string.
    
    """
    params = {
        "select": "licencearea",
        "where": f"sitename = '{sitename}'",
    }
    return await make_request_uk_powernetworks("grid-and-primary-sites", params)


@mcp.tool()
async def regional_power_sites_operational_state_for_sitename(sitename: str) -> str:
    """
    Fetches the regional power siteclassification of UK Power Networks for a specified sitename.
    
    Args:
        sitename (str): The name of the site.

    Returns:
        siteclassification (str): The siteclassification as a string.
    
    """
    params = {
        "select": "siteclassification",
        "where": f"sitename = '{sitename}'",
    }
    return await make_request_uk_powernetworks("grid-and-primary-sites", params)


@mcp.tool()
async def regional_power_sites_asset_type_for_sitename(sitename: str) -> str:
    """
    Fetches the regional power assets of UK Power Networks for a specified sitename.
    
    Args:
        sitename (str): The name of the site.

    Returns:
        siteType (str): The type of the site.
        gridRef (str): The grid reference of the site.
        siteClassification (str): The classification of the site.
    
    """
    params = {
        "select": "sitetype, gridref, siteclassification",
        "where": f"sitename = '{sitename}'",
    }
    return await make_request_uk_powernetworks("grid-and-primary-sites", params)


@mcp.tool()
async def regional_power_sites_nbrsites_for_voltage(sitevoltage: int, preposition: str) -> str:
    """
    Fetches the number of regional power site names of UK Power Networks for a specified voltage level.
    
    Args:
        sitevoltage (int): The voltage level of the site.
        preposition (str): below, above, anything else for equal.

    Returns:
        count(sitename) (int): The number of site names.
    """

    if preposition == "below":
        comparator = "<"
    elif preposition == "above":
        comparator = ">"
    else:
        comparator = "="

    params = {
        "select": "count(sitename) AS number_of_sites ",
        "where": f"sitevoltage {comparator} {sitevoltage}",
    }
    return await make_request_uk_powernetworks("grid-and-primary-sites", params)


@mcp.tool()
async def regional_power_sites_site_type_for_sitename(sitename: str) -> str:
    """
    Fetches the regional power site type of UK Power Networks for a specified sitename.
    
    Args:
        sitename (str): The name of the site.

    Returns:
        sitetype (str): The site type as a string.
    
    """
    params = {
        "select": "sitetype",
        "where": f"sitename = '{sitename}'",
    }
    return await make_request_uk_powernetworks("grid-and-primary-sites", params)


@mcp.tool()
async def regional_power_sites_assesed_for_sitename(sitename: str) -> str:
    """
    Fetches the regional power assessmenent date (YYYY-MM-DD) of UK Power Networks for a specified sitename.
    
    Args:
        sitename (str): The name of the site.

    Returns:
        assessmentdate (str): The assessment date in format YYYY-MM-DD as a string.    
    """
    params = {
        "select": "assessmentdate",
        "where": f"sitename = '{sitename}'",
    }
    return await make_request_uk_powernetworks("grid-and-primary-sites", params)


@mcp.tool()
async def regional_power_sites_resistance_for_sitename(sitename: str) -> str:
    """
    Fetches the measured regional power resistance current of UK Power Networks sites for a specified sitename.
    Args:
        sitename (str): The name of the site.

    Returns:
        measuredresistance_ohm (str): The measured resistance as a string.
    """
    params = {
        "select": "measuredresistance_ohm ",
        "where": f"sitename = '{sitename}'",
    }
    return await make_request_uk_powernetworks("grid-and-primary-sites", params)


# dataset - Secondary Sites

@mcp.tool()
async def secondary_sites_functional_location_for_substation_alias(substationalias: str) -> str:
    """
    Fetches the secondary sites functional location of UK Power Networks Secondary Sites sites for a specified substation alias.

    Args:
        substationalias (str): The alias of the substation.

    Returns:
        functionallocation (str): The functional location as a string.
    """

    params = {
        "select": "functionallocation ",
        "where": f"substationalias  = '{substationalias}'",
    }

    return await make_request_uk_powernetworks("ukpn-secondary-sites", params)

@mcp.tool()
async def secondary_sites_voltage_level_for_substation_alias(substationalias: str) -> str:
    """
    Fetches the secondary sites voltage level metrics of UK Power Networks Secondary Sites sites for a specified substation alias.

    Args:
        substationalias (str): The alias of the substation.

    Returns:
        substationvoltage (str): The substation voltage as a string.
    """

    params = {
        "select": "substationvoltage",
        "where": f"substationalias = '{substationalias}'",
    }

    return await make_request_uk_powernetworks("ukpn-secondary-sites", params)

@mcp.tool()
async def secondary_sites_owner_for_substation_alias(substationalias: str) -> str:
    """
    Fetches the Distribution Network Operator (DNO) and company area of UK Power Networks Secondary Sites sites for a specified substation alias.

    Args:
        substationalias (str): The alias of the substation.

    Returns:
        dno (str): The DNO as a string.
        companyarea (str): The company area as a string.
    """

    params = {
        "select": "dno, companyarea",
        "where": f"substationalias = '{substationalias}'",
    }

    return await make_request_uk_powernetworks("ukpn-secondary-sites", params)

@mcp.tool()
async def secondary_sites_identifiers_for_substation_alias(substationalias: str) -> str:
    """
    Fetches the identifiers of UK Power Networks Secondary Sites sites for a specified substation alias.

    Args:
        substationalias (str): The alias of the substation.

    Returns:
        functional_location (str): The functional location as a string.
        primaryfeederfunctionallocation (str): The primary feeder functional location as a string.
        llsoacode (str): The llsoa code as a string.
        parishcode (str): The parish code as a string.
        postcode (str): The post code as a string.
        geopoint (str): The geo point as a string.
    """

    params = {
        "select": "functionallocation, primaryfeederfunctionallocation, llsoacode, parishcode, postcode, geopoint",
        "where": f"substationalias = '{substationalias}'",
    }

    return await make_request_uk_powernetworks("ukpn-secondary-sites", params)

@mcp.tool()
async def secondary_sites_design_for_substation_alias(substationalias: str) -> str:
    """
    Fetches the design of UK Power Networks Secondary Sites sites for a specified substation alias.

    Args:
        substationalias (str): The alias of the substation.

    Returns:
        substationdesign (str): The substation design as a string.
        indooroutdoor (str): The indoor outdoor as a string.
    """

    params = {
        "select": "substationdesign, indooroutdoor",
        "where": f"substationalias = '{substationalias}'",
    }

    return await make_request_uk_powernetworks("ukpn-secondary-sites", params)


@mcp.tool()
async def secondary_sites_station_for_owner(DNO: str) -> str:
    """
    Fetches a list of stations of UK Power Networks Secondary Sites sites for a specified dno, Distribution Network Operator.
    Ordered by customer count descending and limited to 10 results.

    Args:
        DNO (str): A Distribution Network Operator.

    Returns:
        functional_location (str): functional location as a string.
    """

    params = {
        "select": "functionallocation ",
        "where": f"dno = '{DNO}' ",
        "order_by": "customer_count DESC",
        "limit": 10,
    }

    return await make_request_uk_powernetworks("ukpn-secondary-sites", params)


@mcp.tool()
async def secondary_sites_stations_for_substation_design(substationdesign: str) -> str:
    """
    Fetches a list of stations of UK Power Networks Secondary Sites sites for a specified substation design.
    Ordered by customer count descending and limited to 10 results.
   
     Args:
        substationdesign (str): The design of a substation.

    Returns:
        functional_location (str): functional location as a string.
        customer_count (integer): customer count as an integer.
    """

    params = {
        "select": "functionallocation, customer_count ",
        "where": f"substationdesign = '{substationdesign}' ",
        "order_by": "customer_count DESC ",
        "LIMIT": 10,
    }

    return await make_request_uk_powernetworks("ukpn-secondary-sites", params)

@mcp.tool()
async def secondary_sites_location_for_substation_alias(substationalias: str) -> str:
    """
    Fetches the location of UK Power Networks Secondary Sites sites for a specified substation alias.

    Args:
        substationalias (str): The alias of the substation.

    Returns:
        buildingaddress (str): building address as a string.
        postcode (str): as a string.
        latitude (str): as a string.
        longitude (str): as a string.
    """

    params = {
        "select": "buildingaddress, postcode, latitude, longitude",
        "where": f"substationalias = '{substationalias}'",
    }

    return await make_request_uk_powernetworks("ukpn-secondary-sites", params)

# dataset - Primary Transformers

@mcp.tool()
async def primary_transformer_type_for_site_name(functionallocationname: str) -> str:
    """
    Fetches the type of Primary Site Transformers site for a specified site functional location name.

    Args:
        functionallocationname (str): The site name for a functional location.

    Returns:
        sitetype (str): The sites type as a string.
    """

    params = {
        "select": "sitetype",
        "where": f"functionallocationname = '{functionallocationname}'",
    }

    return await make_request_uk_powernetworks("ukpn-primary-transformers", params)

@mcp.tool()
async def primary_transformer_owner_for_sitename(functionallocationname: str) -> str:
    """
    Fetches the owner (dno) of Primary Site Transformers site for a specified site functional location name.

    Args:
        functionallocationname (str): The site functional location.

    Returns:
        dno (str): A Distribution Network Operator.
    """

    params = {
        "select": "dno",
        "where": f"functionallocationname = '{functionallocationname}'",
    }

    return await make_request_uk_powernetworks("ukpn-primary-transformers", params)


@mcp.tool()
async def primary_transformer_description_for_site_name(functionallocationname: str) -> str:
    """
    Fetches the description of Primary Site Transformers site for a specified site functional location name.

    Args:
        functionallocationname (str): The site functional location.

    Returns:
        sitedesc (str): The site description.
    """

    params = {
        "select": "sitedesc",
        "where": f"functionallocationname = '{functionallocationname}'",
    }

    return await make_request_uk_powernetworks("ukpn-primary-transformers", params)


if __name__ == "__main__":
    mcp.run(transport='stdio')
