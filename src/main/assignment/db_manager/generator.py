from datetime import date
import pandas as pd
import random
from typing import List
import uuid
from .utils import _get_next_month
from .utils import _get_previous_month
from .utils import _random_date
from .server import Server


class Generator:
    """Class to Generate the fake data
    """

    def __init__(
        self,
        starting_date: date,
        nb_company: int,
        nb_month=12,
        frac_small_company=0.70
    ) -> None:
        """ Intinitilisation of the Generator to get the Fake Data

        Args:
            starting_date (date): Date when we want to start to generate data
            nb_company (int): the size of company to create at the month X
            nb_month (int, optional): how many month do we want the sessions
            information. Defaults to 12.
            frac_small_company (float, optional): Percentage of small company.
            Defaults to 0.70.
        """
        self.starting_date = starting_date
        self.nb_company = nb_company
        self.nb_month = nb_month
        self.frac_small_company = frac_small_company
        self.company_information = self._get_company_information()
        self.session_information = self._get_session_information()

    def _get_company_information(self) -> pd.DataFrame:
        """Get the company information from the Generator exercice

        Returns:
            pd.DataFrame: company_information
        """
        # Create fake database for the starting date
        company_information = pd.DataFrame({
            'company_id': [i for i in range(1, self.nb_company + 1)],
            'created_at': [
                self.starting_date for i in range(1, self.nb_company + 1)
            ],
            'company_size': ['large' for i in range(1, self.nb_company + 1)]
        })

        # randomly 70% of the DataFrame to put the company_size = 'small'
        small_company_id = company_information.sample(
            frac=self.frac_small_company
        ).company_id.tolist()
        company_information.loc[
            company_information.company_id.isin(small_company_id),
            'company_size'
        ] = 'small'
        return company_information

    def _get_session_information(self) -> pd.DataFrame:
        """Get the all session got the required timeline

        Returns:
            pd.DataFrame: session_information
        """
        list_sessions_information = []
        current_month = self.starting_date
        for i in range(0, self.nb_month):
            # Get the session information for the current month
            current_session_information = self._get_session_table(
                current_month,
                list_sessions_information
            )
            # Append to the list
            list_sessions_information.append(current_session_information)
            # Iteration for th next month
            current_month = _get_next_month(current_month)
        return pd.concat(list_sessions_information)

    def _get_session_table(
        self,
        current_month: date,
        list_sessions_information: List[pd.DataFrame]
    ) -> pd.DataFrame:
        """ Get the session table for a specifics month.

        Args:
            current_month (date): the company_information table

        Returns:
            pd.DataFrame: session_information of the current month
        """
        # Setup the session information table if first iteration
        if current_month == self.starting_date:
            active_company = self.company_information.company_id.tolist()

        # look the month which company has been active
        else:
            tmp = pd.concat(list_sessions_information)
            active_company = tmp[
                tmp.created_at > _get_previous_month(
                    current_month
                )
            ].company_id.unique().tolist()

        # get the list of company we are going to work on.
        session_information = self.company_information[
            self.company_information.company_id.isin(active_company)
        ][[
            'company_id', 'company_size'
        ]].copy()

        session_information['created_at'] = session_information \
            .company_size \
            .apply(
                lambda x: self._get_sessions(x, current_month)
        )
        session_information = session_information.explode('created_at')
        session_information.drop(columns=['company_size'], inplace=True)
        session_information['session_id'] = session_information.apply(
            lambda x: str(uuid.uuid4().int)[:15],
            axis=1
        )
        # Keep only at least one session
        session_information = session_information[
            ~session_information.created_at.isna()
        ]

        return session_information

    def _get_sessions(
        self,
        company_size: str,
        current_month: date
    ) -> List[date]:
        """Get the session for a specifics company depending in its size.

        Args:
            company_size (str): small or large.
            current_month (date): current ot the sessions generation

        Returns:
            List[date]: List of date for each session
            Can be an empty list if no session for this company.
        """
        # get the random bracket of session depending on the company size
        if company_size == 'small':
            random_bracket = 5
        elif company_size == 'large':
            random_bracket = 10

        # get the number of session
        number_session = random_bracket + \
            random.randrange(-random_bracket, random_bracket)

        # get the list of date, each date correspond to one session
        sessions = [
            _random_date(current_month, _get_next_month(current_month))
            for i in range(1, number_session + 1)
        ]
        return sessions

    def send_to_database(
        self,
        server: Server
    ) -> int:
        server.db['abc'].tb['company_information'].append_dataframe(
            self.company_information
        )
        server.db['abc'].tb['session_information'].append_dataframe(
            self.session_information
        )
        return 1

    def delete_from_database(
        self,
        server: Server
    ) -> int:
        query = """
            delete from abc.company_information
        """
        return server._execute_action(query)
