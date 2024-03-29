import requests
import xml.etree.ElementTree as ET
#CRUD ops on the database
class DataverseError(Exception):
    def __init__(self, message, status_code=None, response=None):
        super().__init__(message)
        self.status_code = status_code
        self.response = response

class DataverseORM:
    def __init__(self, dynamics_url, access_token, refresh_token_callback=None):
        self.dynamics_url = dynamics_url
        self.headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json",
            "OData-Version": "4.0",
            "OData-MaxVersion": "4.0",
            "Prefer": "return=representation, odata.include-annotations=OData.Community.Display.V1.FormattedValue"
        }
        self.base_url = f"{dynamics_url}/api/data/v9.2/"
        #self.metadata_validation = metadata_validation
        self._entity_cache = {}
        self.refresh_token_callback = refresh_token_callback

    def handle_token_expiration_error(self, error):
        if error.response.status_code == 401 and self.refresh_token_callback:
            # Refresh the access token
            new_access_token = self.refresh_token_callback()
            self.access_token(new_access_token)
            return True
        return False

    def entity(self, entity_name):
        if entity_name not in self._entity_cache:
            self._entity_cache[entity_name] = Entity(self, entity_name)
        return self._entity_cache[entity_name]

class Entity:
    def __init__(self, orm, entity_name):
        self.orm = orm
        self.entity_name = entity_name
        # if orm.metadata_validation:
        #     self.entity_set, self.entity_type_element = self._validate_entity()


    def get(self, entity_id):
        url = f"{self.orm.base_url}{self.entity_name}({entity_id})"
        try:
            response = requests.get(url, headers=self.orm.headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
                if self.orm.handle_token_expiration_error(e):
                    return self.get(entity_id)
                else:
                    raise DataverseError(f"Error getting entity: {e}", response=e.response)

    def create(self, entity_data):
        # self._validate_properties(entity_data)
        url = f"{self.orm.base_url}{self.entity_name}"
        try:
            response = requests.post(url, headers=self.orm.headers, json=entity_data)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            if self.orm.handle_token_expiration_error(e):
                return self.create(entity_data)
            raise DataverseError(f"Error creating entity: {e}", response=e.response)

    def update(self, entity_id, entity_data):
        url = f"{self.orm.base_url}{self.entity_name}({entity_id})"
        try:
            response = requests.patch(url, headers=self.orm.headers, json=entity_data)
            response.raise_for_status()
            return response.status_code == 204
        except requests.exceptions.RequestException as e:
            if self.orm.handle_token_expiration_error(e):
                return self.update(entity_id, entity_data)
            raise DataverseError(f"Error updating entity: {e}", response=e.response)

    def delete(self, entity_id):
        url = f"{self.orm.base_url}{self.entity_name}({entity_id})"
        try:
            response = requests.delete(url, headers=self.orm.headers)
            response.raise_for_status()
            return response.status_code == 204
        except requests.exceptions.RequestException as e:
            if(self.orm.handle_token_expiration_error(e)):
                return self.delete(entity_id)
            raise DataverseError(f"Error deleting entity: {e}", response=e.response)

    def query(self, filter_expression=None, select_fields=None, order_by=None):
        url = f"{self.orm.base_url}{self.entity_name}"
        params = {}

        if filter_expression:
            params["$filter"] = filter_expression
        if select_fields:
            params["$select"] = ",".join(select_fields)
        if order_by:
            params["$orderby"] = order_by

        try:
            response = requests.get(url, headers=self.orm.headers, params=params)
            response.raise_for_status()
            return response.json()["value"]
        except requests.exceptions.RequestException as e:
            if(self.orm.handle_token_expiration_error(e)):
                return self.query(filter_expression, select_fields, order_by)
            raise DataverseError(f"Error querying entity: {e}", response=e.response)
    '''
    def audit(self, entity_id, value):
        name = self.entity_name[:-1]
        url = f"{self.orm.base_url}RetrieveRecordChangeHistory(Target=@Target)?@Target="+'{'+f"{entity_id}:'{value}',@odata.type:'Microsoft.Dynamics.CRM.{name}'"+'}'
        
        params = {
            entity_id: value,
            "@odata.type":"Microsoft.Dynamics.CRM."+self.entity_name
        }
        try:
            response = requests.get(url, headers=self.orm.headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
                if self.orm.handle_token_expiration_error(e):
                    return self.get(entity_id)
                else:
                    raise DataverseError(f"Error getting entity: {e}", response=e.response)
    '''

    def audit(self, filter_expression):
        name = self.entity_name[:-1]
        url = f"{self.orm.base_url}audits"
        params = {}
        params["$filter"] = filter_expression
        print("Params: ", params["$filter"])
        try:
            response = requests.get(url, headers=self.orm.headers, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
                if self.orm.handle_token_expiration_error(e):
                    return self.query(filter_expression)
                else:
                    raise DataverseError(f"Error getting entity: {e}", response=e.response)