class Status(object):
    """
    Scheme approval base class. Maintains shared attributes and methods
    """
    def __init__(self):
        self._checked_ids = self._workflow_pks = None
        self.data_service = self._lookup = None

    def set_check_ids(self, checked_ids):
        """
        Sets checked scheme record IDs
        :param checked_ids: Checked scheme record IDs
        :type checked_ids: OrderedDict
        """
        self._checked_ids = checked_ids

    def _checked_scheme_ids(self, status_option):
        """
        Return checked scheme IDs
        :return scheme_ids: Checked scheme IDs/primary keys
        :rtype scheme_ids: List
        """
        scheme_ids = [
            scheme_id for scheme_id, (row, status, scheme_number) in
            self._checked_ids.iteritems() if int(status) != status_option
        ]
        return scheme_ids

    def _approved_scheme_ids(self, approved_items):
        """
        Return checked approved scheme IDs
        :param approved_items: Approved work flow update values, columns and filters
        :type approved_items: Dictionary
        :return scheme_ids: Checked approved scheme IDs/primary keys
        :rtype scheme_ids: List
        """
        scheme_ids = [
            scheme_id for scheme_id, (row, status, scheme_number) in
            self._checked_ids.iteritems() if row in approved_items
        ]
        return scheme_ids

    @property
    def _workflow_ids(self):
        """
        Returns workflow IDs/primary keys
        :return _workflow_pks: Workflow record ID/primary keys
        :rtype _workflow_pks: Dictionary
        """
        if self._workflow_pks is None:
            self._workflow_pks = self.data_service.workflow_ids()
        return self._workflow_pks

    def _scheme_workflow_filter(self, scheme_id, workflow_id):
        """
        Scheme workflow update/query filters
        :param scheme_id: Scheme record id
        :type scheme_id: Integer
        :param workflow_id: Workflow record id
        :type workflow_id: Integer
        :return workflow_filter: Workflow type data filter
        :rtype workflow_filter: Dictionary
        """
        workflow_filter = {
            self._lookup.SCHEME_COLUMN: scheme_id,
            self._lookup.WORKFLOW_COLUMN: workflow_id
        }
        return workflow_filter

    def _filter_in(self, entity_name, filters):
        """
        Return query objects as a collection of filter using in_ operator
        :param entity_name: Name of entity to be queried
        :type entity_name: String
        :param filters: Query filter columns and values
        :type filters: Dictionary
        :return: Query object results
        :rtype: InstrumentedList
        """
        return self.data_service.filter_in(entity_name, filters).all()

    def scheme_workflow_id(self, query, column, scheme_id, workflow_ids):
        """
        Return scheme workflow record IDs
        :return query: Query results
        :type query: InstrumentedList
        :param column: Column name
        :param column: String
        :param scheme_id: Scheme record ID
        :type scheme_id: Integer
        :param workflow_ids: Workflow record ID
        :type workflow_ids: List
        :return record_ids: Scheme workflow record ID
        :return record_ids: Dictionary
        """
        record_ids = {}
        for q in query:
            q_scheme_id = getattr(q, self._lookup.SCHEME_COLUMN, None)
            q_workflow_id = getattr(q, self._lookup.WORKFLOW_COLUMN, None)
            if q_scheme_id == scheme_id:
                if q_workflow_id in workflow_ids:
                    record_ids[q_workflow_id] = getattr(q, column, None)
        return record_ids

    @ staticmethod
    def _get_config_option(config):
        """
        Returns save/update configuration options
        :param config: Save/update configuration options
        :type config: Named
        :return option: Save/update configuration option
        :rtype option: named tuple
        """
        for option in config:
            yield option

    @staticmethod
    def to_list(data):
        """
        Casts data to type List
        :param data: Input data
        :param data: Object
        :return: List data type
        :rtype: List
        """
        if data and not isinstance(data, list):
            data = [data]
        return data

    @staticmethod
    def valid_items(items, value):
        """
        Checks if items are valid
        :param items: List items
        :type items: List
        :param value: Value to validated against
        :param value: Object
        :return: True or False
        :return: Boolean
        """
        if not items:
            return False
        return all([True if item == value else False for item in items])


class Approve(Status):
    """
    Manages scheme approval in Scheme Establishment, First, Second,
    and Third Examination and Import Plot and Scheme Revision FLTS workflows
    """
    def __init__(self, data_service, object_name):
        super(Approve, self).__init__()
        self.data_service = data_service
        self._lookup = self.data_service.lookups
        self._checked_ids = None
        self._object_name = object_name
        self._workflow_filter = None
        self._update_columns = self.data_service.update_columns
        self._save_columns = self.data_service.save_columns
        self._next_workflows_updates = {}
        self._new_workflows_data = {}

    def workflow_approvals(self, status_option):
        """
        Returns current workflow approval update values, columns and filters
        :param status_option: Approve status
        :type status_option: Integer
        :return valid_approvals: Valid approval update values, columns and filters
        :rtype valid_approvals: Dictionary
        :rtype scheme_numbers: Dictionary
        :rtype scheme_numbers: Dictionary
        """
        valid_approvals = {}
        scheme_numbers = {"valid": [], "invalid": []}
        scheme_ids = self._checked_scheme_ids(status_option)
        prev_workflow_ids = self._prev_workflow_ids()
        filters = self._scheme_workflow_filter(scheme_ids, prev_workflow_ids)
        query_objects = self._filter_in("Scheme_workflow", filters)  # TODO: Place name in the config file
        for scheme_id, (row, status, scheme_number) in self._checked_ids.iteritems():
            if int(status) == status_option:
                continue
            prev_approval_ids = self.scheme_workflow_id(
                query_objects, self._lookup.APPROVAL_COLUMN,
                scheme_id, prev_workflow_ids
            )
            approvals = self._workflow_updates(
                prev_approval_ids, scheme_id, status_option
            )
            if approvals:
                valid_approvals[row] = approvals
                scheme_numbers["valid"].append(scheme_number)
                continue
            scheme_numbers["invalid"].append((scheme_number, prev_approval_ids))
        return valid_approvals, scheme_numbers

    def _prev_workflow_ids(self):
        """
        Return preceding workflow record IDs
        :return workflow_id: Preceding workflow record IDs
        :rtype workflow_id: List
        """
        workflow_id = self._get_workflow_id()
        workflow_id = self._workflow_ids[workflow_id][0]
        return workflow_id

    def _workflow_updates(self, approval_ids, scheme_id, status):
        """
        Return valid current workflow approval update values, columns and filters
        :param approval_ids: Preceding workflow approval record IDs
        :type approval_ids: Dictionary
        :param scheme_id: Checked item scheme record ID
        :type scheme_id: Integer
        :param status: Approve record ID status
        :type status: Integer
        :return updates: Valid approval update values, columns and filters
        :rtype updates: List
        """
        # TODO: Start Refactor. Refer to _disapproval_updates
        updates = []
        approval_ids = approval_ids.values()
        for column in self._get_config_option(self._update_columns):
            if self.valid_items(approval_ids, status) or \
                    self._object_name == "schemeLodgement":
                update_filters = self._scheme_workflow_filter(
                    scheme_id, self._get_workflow_id()
                )
                updates.append([column.column, status, update_filters])
        return updates

    def next_workflow_approvals(self, approved_items):
        """
        Returns succeeding workflow approval update values, columns and filters
        :param approved_items: Approved work flow update values, columns and filters
        :type approved_items: Dictionary
        :return workflow_approvals: Succeeding workflow approval update values, columns and filters
        :rtype workflow_approvals: Dictionary
        """
        workflow_approvals = {}
        next_workflow_ids = self._next_workflow_ids()
        scheme_ids = self._approved_scheme_ids(approved_items)
        filters = self._scheme_workflow_filter(scheme_ids, next_workflow_ids)
        query_objects = self._filter_in("Scheme_workflow", filters)  # TODO: Place name in the config file
        self._reset_next_workflows()
        for scheme_id, (row, status, scheme_number) in self._checked_ids.iteritems():
            if row in approved_items:
                workflow_id = self.scheme_workflow_id(
                    query_objects, self._lookup.WORKFLOW_COLUMN,
                    scheme_id, next_workflow_ids
                )
                if workflow_id:
                    approvals = self._next_workflow_updates(next_workflow_ids, scheme_id)
                    self._set_next_workflows(self._next_workflows_updates, row, approvals)
                else:
                    approvals = self._new_workflow_data(next_workflow_ids, scheme_id)
                    self._set_next_workflows(self._new_workflows_data, row, approvals)
        return workflow_approvals

    def _next_workflow_ids(self):
        """
        Return succeeding workflow record IDs
        :return workflow_id: Succeeding workflow record IDs
        :rtype workflow_id: List
        """
        workflow_id = self._get_workflow_id()
        workflow_id = self._workflow_ids[workflow_id][1]
        return workflow_id

    def _next_workflow_updates(self, workflow_ids, scheme_id):
        """
        Returns succeeding workflow approval update values, columns and filters
        :param workflow_ids: Succeeding workflow record IDs
        :type workflow_ids: List
        :param scheme_id: Scheme ID
        :type scheme_id: Integer
        :return updates: Succeeding workflow approval update values, columns and filters
        :rtype updates: List
        """
        updates = []
        for workflow_id in workflow_ids:
            update = []
            for column in self._get_config_option(self._update_columns):
                column = column.column
                filters = self._scheme_workflow_filter(scheme_id, workflow_id)
                update.append([column, self._lookup.PENDING(), filters])
            updates.append(update)
        return updates

    def _new_workflow_data(self, workflow_ids, scheme_id):
        """
        Returns new workflow data values, columns and entity
        :param workflow_ids: New workflow record IDs
        :type workflow_ids: List
        :param scheme_id: New workflow scheme ID
        :type scheme_id: Integer
        :return save_data: Items to be saved
        :rtype save_data: List
        """
        save_data = []
        for workflow_id in workflow_ids:
            items = []
            for option in self._get_config_option(self._save_columns):
                column = option.column
                column_name = self._get_dict_value(column)
                if column_name == self._lookup.WORKFLOW_COLUMN:
                    value = workflow_id
                elif column_name == self._lookup.SCHEME_COLUMN:
                    value = scheme_id
                else:
                    value = self._lookup.PENDING()
                items.append([column, value, option.entity])
            save_data.append(items)
        return save_data

    @staticmethod
    def _get_dict_value(attr):
        """
        Returns values of a dictionary
        :param attr: Attribute
        :return: Attribute value
        :rtype: Dictionary/non-dictionary
        """
        if isinstance(attr, dict):
            value = attr.values()
            if len(value) == 1:
                value = value[0]
            return value
        return attr

    def _set_next_workflows(self, container, key, approvals):
        """
        Sets the succeeding workflows updates/new data
        :param container: Data container
        :type container: Dictionary
        :param key: Data value identifier
        :param key: Integer
        :param approvals: Data value
        :param approvals: List
        """
        current_workflow_id = self._get_workflow_id()
        if approvals and current_workflow_id != next(reversed(self._workflow_ids)):
            container[key] = tuple(approvals)

    def _get_workflow_id(self):
        """
        Return workflow id/primary key
        :return: Workflow id/primary key
        :rtype: Integer
        """
        if self._workflow_filter:
            return self._workflow_filter[self._lookup.WORKFLOW_COLUMN]
        return self.data_service.get_workflow_id(self._object_name)

    def _reset_next_workflows(self):
        """
        Resets the succeeding workflows data contaners
        :return:
        """
        self._next_workflows_updates = {}
        self._new_workflows_data = {}

    @property
    def next_workflows_updates(self):
        """
        Returns the succeeding next workflows updates
        :return _next_workflows_updates: Next workflows updates
        :rtype _next_workflows_updates: Dictionary
        """
        return self._next_workflows_updates

    @property
    def new_workflows_data(self):
        """
        Returns new workflows data
        :return _new_workflows_data: New workflows data
        :rtype _new_workflows_data: Dictionary
        """
        return self._new_workflows_data


class Disapprove(Status):
    """
    Manages scheme disapproval in Scheme Establishment and
    First, Second and Third Examination FLTS workflows
    """
    def __init__(self, data_service):
        super(Disapprove, self).__init__()
        self.data_service = data_service
        self._lookup = self.data_service.lookups
        self._checked_ids = None
        self._update_columns = self.data_service.update_columns

    def disapprove_items(self, status_option):
        """
        Returns workflow disapprove update values, columns and filters
        :param status_option: Disapprove status
        :type status_option: Integer
        :return valid_items: Disapprove update values, columns and filters
        :rtype valid_items: Dictionary
        """
        valid_items = {}
        scheme_numbers = []
        scheme_ids = self._checked_scheme_ids(status_option)
        # filters = self._scheme_workflow_filter(scheme_ids, self._workflow_ids)
        filters = self._scheme_workflow_filter(scheme_ids, self._workflow_ids.keys())
        query_objects = self._filter_in("Scheme_workflow", filters)  # TODO: Place name in the config file
        for scheme_id, (row, status, scheme_number) in \
                self._checked_ids.iteritems():
            if int(status) != status_option:
                # workflow_ids = self.scheme_workflow_id(
                #     query_objects, self._lookup.WORKFLOW_COLUMN,
                #     scheme_id, self._workflow_ids
                # )
                workflow_ids = self.scheme_workflow_id(
                    query_objects, self._lookup.WORKFLOW_COLUMN,
                    scheme_id, self._workflow_ids.keys()
                )
                update_items = self._disapproval_updates(
                    workflow_ids, scheme_id, status_option
                )
                if update_items:
                    valid_items[row] = update_items
                    scheme_numbers.append(scheme_number)
        return valid_items, scheme_numbers

    def _disapproval_updates(self, workflow_ids, record_id, status):
        """
        Return disapproval update items
        :param workflow_ids: Preceding and succeeding workflow record IDs
        :type workflow_ids: List
        :param record_id: Checked items scheme record ID
        :type record_id: Integer
        :param status: Disapprove record ID status
        :type status: Integer
        :return update_items: Disapproval update items
        :rtype update_items: List
        """
        # TODO: Start Refactor. Refer to _approval_updates
        update_items = []
        for updates in self._get_config_option(self._update_columns):
            for workflow_id in workflow_ids:
                if workflow_id is not None:
                    update_filters = self._scheme_workflow_filter(
                        record_id, workflow_id
                    )
                    # TODO: Start Refactor
                    # value = status
                    # if updates.value:
                    #     value = updates.value
                    # update_items.append([updates.column, value, update_filters])
                    # TODO: End Refactor
                    update_items.append([updates.column, status, update_filters])
        return update_items
        # TODO: End Refactor. Refer to _approval_updates
