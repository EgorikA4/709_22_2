"""SQL queries."""
GET_PROPERTIES = """
    with
        properties_with_hcs as (
            select
                p.id,
                coalesce(json_agg(json_build_object(
                    'id', hcs.id, 'name', hcs.name, 'phone', hcs.phone,
                    'address', hcs.address, 'capital', hcs.capital
                ))
                    filter (where hcs.id is not null), '[]') as hcs
            from api_data.properties as p
            left join api_data.hcs on p.hcs_id = api_data.hcs.id
            group by p.id
        ),
        properties_with_owners as (
            select
                p.id,
                p.address,
                p.square,
                p.price,
                coalesce(json_agg(json_build_object(
                    'id', owners.id, 'first_name', owners.first_name,
                    'last_name', owners.last_name, 'passport', owners.passport
                ))
                    filter (where owners.id is not null), '[]')
                    as owners
            from api_data.properties as p
            left join api_data.owners_properties as op\
                on op.properties_id = p.id
            left join api_data.owners on op.owners_id = api_data.owners.id
            group by p.id
        )


    select
        pwo.id,
        address,
        square,
        price,
        owners,
        hcs
    from properties_with_owners as pwo
    join properties_with_hcs as pwh on pwo.id = pwh.id;
    """

GET_PROPERTIES_BY_PRICE = """
    with
        properties_with_hcs as (
            select
                p.id,
                coalesce(json_agg(json_build_object(
                    'id', hcs.id, 'name', hcs.name, 'phone', hcs.phone,
                    'address', hcs.address, 'capital', hcs.capital
                ))
                    filter (where hcs.id is not null), '[]') as hcs
            from api_data.properties as p
            left join api_data.hcs on p.hcs_id = api_data.hcs.id
            group by p.id
        ),
        properties_with_owners as (
            select
                p.id,
                p.address,
                p.square,
                p.price,
                coalesce(json_agg(json_build_object(
                    'id', owners.id, 'first_name', owners.first_name,
                    'last_name', owners.last_name, 'passport', owners.passport
                ))
                    filter (where owners.id is not null), '[]')
                    as owners
            from api_data.properties as p
            left join api_data.owners_properties as op\
                on op.properties_id = p.id
            left join api_data.owners on op.owners_id = api_data.owners.id
            group by p.id
        )


    select
        pwo.id,
        address,
        square,
        price,
        owners,
        hcs
    from properties_with_owners as pwo
    join properties_with_hcs as pwh on pwo.id = pwh.id
    where price >= {price_lower_bound} and price <= {price_upper_bound};
    """

GET_PROPERTIES_BY_ADDRESS = """
    with
        properties_with_hcs as (
            select
                p.id,
                coalesce(json_agg(json_build_object(
                    'id', hcs.id, 'name', hcs.name, 'phone', hcs.phone,
                    'address', hcs.address, 'capital', hcs.capital
                ))
                    filter (where hcs.id is not null), '[]') as hcs
            from api_data.properties as p
            left join api_data.hcs on p.hcs_id = api_data.hcs.id
            group by p.id
        ),
        properties_with_owners as (
            select
                p.id,
                p.address,
                p.square,
                p.price,
                coalesce(json_agg(json_build_object(
                    'id', owners.id, 'first_name', owners.first_name,
                    'last_name', owners.last_name, 'passport', owners.passport
                ))
                    filter (where owners.id is not null), '[]')
                    as owners
            from api_data.properties as p
            left join api_data.owners_properties as op\
                on op.properties_id = p.id
            left join api_data.owners on op.owners_id = api_data.owners.id
            group by p.id
        )


    select
        pwo.id,
        address,
        square,
        price,
        owners,
        hcs
    from properties_with_owners as pwo
    join properties_with_hcs as pwh on pwo.id = pwh.id
    where address ilike {address};
    """

GET_ENTITY = 'select id from api_data.{table} where id = {id_};'

CREATE_PROPERTIES = """
    insert into api_data.properties (address, square, price, hcs_id)
    values ({address}, {square}, {price}, {hcs_id})
    returning id;
"""

UPDATE_PROPERTIES = """
    update api_data.properties
    set
        address = {address},
        square = {square},
        price = {price},
        hcs_id = {hcs_id}
    where id = {id_}
    returning id;
"""

GET_HCS_ID = 'select hcs_id from api_data.properties where id = {id_}'

DELETE_PROPERTIES_LINKS = """
    delete from api_data.owners_properties where properties_id = {id_}
"""

DELETE_PROPERTIES = """
    delete from api_data.properties where id = {id_}
    returning id;
"""
