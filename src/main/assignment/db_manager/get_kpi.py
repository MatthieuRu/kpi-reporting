import pandas as pd
from .server import Server


def get_kpi_usage(server: Server) -> pd.DataFrame:
    query = """
        select
            period,
            (nb_session / nb_company) as nb_average_session,
            company_size
        from (
            select
                date_trunc('month', si.created_at)::date as period,
                count(distinct ci.company_id) as nb_company,
                count(distinct si.session_id) as nb_session,
                ci.company_size as company_size
            from abc.session_information as si
            inner join abc.company_information as ci
            on ci.company_id = si.company_id
            group by period, company_size
        ) as subquery;
    """
    return server._execute_extract(query)


def get_kpi_retention(server: Server) -> pd.DataFrame:
    query = """
        select
            period,
            count(distinct company_id) as nb_company,
            company_size
        from (
            select
                date_trunc('month', si.created_at)::date as period,
                ci.company_id as company_id,
                ci.company_size as company_size
            from abc.session_information as si
            inner join abc.company_information as ci
            on si.company_id = ci.company_id
        ) as subquery
        group by period, company_size;
    """
    return server._execute_extract(query)


def get_kpi_revenue(server: Server) -> pd.DataFrame:
    query = """
        select
            period,
            count(distinct company_id) * 99 as revenu,
            company_size
        from (
            select
                date_trunc('month', si.created_at)::date as period,
                ci.company_id as company_id,
                ci.company_size as company_size
            from abc.session_information as si
            inner join abc.company_information as ci
            on si.company_id = ci.company_id
        ) as subquery
        where company_size = 'large'
        group by period, company_size
        union all
        select
            period,
            count(distinct company_id) * 19 as revenu,
            company_size
        from (
            select
                date_trunc('month', si.created_at)::date as period,
                ci.company_id as company_id,
                ci.company_size as company_size
            from abc.session_information as si
            inner join abc.company_information as ci
            on si.company_id = ci.company_id
        ) as subquery
        where company_size = 'small'
        group by period, company_size
    """
    return server._execute_extract(query)
