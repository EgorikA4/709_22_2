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
            from properties as p
            left join hcs on p.hcs_id = hcs.id
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
                    filter (where owners.id is not null), '[]') as owners
            from properties as p
            left join owners_properties as op on op.properties_id = p.id
            left join owners on op.owners_id = owners.id
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
GET_ENTITY = 'select id from {table} where id = {id_};'

CREATE_PROPERTIES = """
    insert into properties (address, square, price, hcs_id)
    values ({address}, {square}, {price}, {hcs_id})
    returning id;
"""

UPDATE_PROPERTIES = """
    update properties
    set
        address = {address},
        square = {square},
        price = {price},
        hcs_id = {hcs_id}
    where id = {id_}
    returning id;
"""

GET_HCS_ID = 'select hcs_id from properties where id = {id_}'

DELETE_PROPERTIES_LINKS = """
    delete from owners_properties where properties_id = {id_}
"""

DELETE_PROPERTIES = """
    delete from properties where id = {id_}
    returning id;
"""
