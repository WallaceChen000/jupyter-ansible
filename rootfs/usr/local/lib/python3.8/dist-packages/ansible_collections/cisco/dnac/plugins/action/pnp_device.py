#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (c) 2021, Cisco Systems
# GNU General Public License v3.0+ (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type
from ansible.plugins.action import ActionBase
try:
    from ansible_collections.ansible.utils.plugins.module_utils.common.argspec_validate import (
        AnsibleArgSpecValidator,
    )
except ImportError:
    ANSIBLE_UTILS_IS_INSTALLED = False
else:
    ANSIBLE_UTILS_IS_INSTALLED = True
from ansible.errors import AnsibleActionFail
from ansible_collections.cisco.dnac.plugins.plugin_utils.dnac import (
    DNACSDK,
    dnac_argument_spec,
    dnac_compare_equality,
    get_dict_result,
)
from ansible_collections.cisco.dnac.plugins.plugin_utils.exceptions import (
    InconsistentParameters,
)

# Get common arguments specification
argument_spec = dnac_argument_spec()
# Add arguments specific for this module
argument_spec.update(dict(
    state=dict(type="str", default="present", choices=["present", "absent"]),
    _id=dict(type="str"),
    deviceInfo=dict(type="dict"),
    runSummaryList=dict(type="list"),
    systemResetWorkflow=dict(type="dict"),
    systemWorkflow=dict(type="dict"),
    tenantId=dict(type="str"),
    version=dict(type="int"),
    workflow=dict(type="dict"),
    workflowParameters=dict(type="dict"),
    id=dict(type="str"),
))

required_if = [
    ("state", "present", ["id", "deviceInfo"], True),
    ("state", "absent", ["id", "deviceInfo"], True),
]
required_one_of = []
mutually_exclusive = []
required_together = []


class PnpDevice(object):
    def __init__(self, params, dnac):
        self.dnac = dnac
        self.new_object = dict(
            _id=params.get("_id"),
            deviceInfo=params.get("deviceInfo"),
            runSummaryList=params.get("runSummaryList"),
            systemResetWorkflow=params.get("systemResetWorkflow"),
            systemWorkflow=params.get("systemWorkflow"),
            tenantId=params.get("tenantId"),
            version=params.get("version"),
            workflow=params.get("workflow"),
            workflowParameters=params.get("workflowParameters"),
            id=params.get("id"),
        )

    def get_all_params(self, name=None, id=None):
        new_object_params = {}
        new_object_params['limit'] = self.new_object.get('limit')
        new_object_params['offset'] = self.new_object.get('offset')
        new_object_params['sort'] = self.new_object.get('sort')
        new_object_params['sort_order'] = self.new_object.get('sortOrder') or \
            self.new_object.get('sort_order')
        new_object_params['serial_number'] = self.new_object.get('serialNumber') or \
            self.new_object.get('serial_number')
        new_object_params['state'] = self.new_object.get('state_') or \
            self.new_object.get('state')
        new_object_params['onb_state'] = self.new_object.get('onbState') or \
            self.new_object.get('onb_state')
        new_object_params['cm_state'] = self.new_object.get('cmState') or \
            self.new_object.get('cm_state')
        new_object_params['name'] = name or self.new_object.get('name')
        new_object_params['pid'] = self.new_object.get('pid')
        new_object_params['source'] = self.new_object.get('source')
        new_object_params['project_id'] = self.new_object.get('projectId') or \
            self.new_object.get('project_id')
        new_object_params['workflow_id'] = self.new_object.get('workflowId') or \
            self.new_object.get('workflow_id')
        new_object_params['project_name'] = self.new_object.get('projectName') or \
            self.new_object.get('project_name')
        new_object_params['workflow_name'] = self.new_object.get('workflowName') or \
            self.new_object.get('workflow_name')
        new_object_params['smart_account_id'] = self.new_object.get('smartAccountId') or \
            self.new_object.get('smart_account_id')
        new_object_params['virtual_account_id'] = self.new_object.get('virtualAccountId') or \
            self.new_object.get('virtual_account_id')
        new_object_params['last_contact'] = self.new_object.get('lastContact') or \
            self.new_object.get('last_contact')
        new_object_params['mac_address'] = self.new_object.get('macAddress') or \
            self.new_object.get('mac_address')
        new_object_params['hostname'] = self.new_object.get('hostname')
        new_object_params['site_name'] = self.new_object.get('siteName') or \
            self.new_object.get('site_name')
        return new_object_params

    def create_params(self):
        new_object_params = {}
        new_object_params['_id'] = self.new_object.get('_id')
        new_object_params['deviceInfo'] = self.new_object.get('deviceInfo')
        new_object_params['runSummaryList'] = self.new_object.get('runSummaryList')
        new_object_params['systemResetWorkflow'] = self.new_object.get('systemResetWorkflow')
        new_object_params['systemWorkflow'] = self.new_object.get('systemWorkflow')
        new_object_params['tenantId'] = self.new_object.get('tenantId')
        new_object_params['version'] = self.new_object.get('version')
        new_object_params['workflow'] = self.new_object.get('workflow')
        new_object_params['workflowParameters'] = self.new_object.get('workflowParameters')
        return new_object_params

    def delete_by_id_params(self):
        new_object_params = {}
        new_object_params['id'] = self.new_object.get('id')
        return new_object_params

    def update_by_id_params(self):
        new_object_params = {}
        new_object_params['_id'] = self.new_object.get('_id')
        new_object_params['deviceInfo'] = self.new_object.get('deviceInfo')
        new_object_params['runSummaryList'] = self.new_object.get('runSummaryList')
        new_object_params['systemResetWorkflow'] = self.new_object.get('systemResetWorkflow')
        new_object_params['systemWorkflow'] = self.new_object.get('systemWorkflow')
        new_object_params['tenantId'] = self.new_object.get('tenantId')
        new_object_params['version'] = self.new_object.get('version')
        new_object_params['workflow'] = self.new_object.get('workflow')
        new_object_params['workflowParameters'] = self.new_object.get('workflowParameters')
        new_object_params['id'] = self.new_object.get('id')
        return new_object_params

    def get_object_by_name(self, name):
        result = None
        # NOTE: Does not have a get by name method or it is in another action
        try:
            items = self.dnac.exec(
                family="device_onboarding_pnp",
                function="get_device_list",
                params=self.get_all_params(name=name),
            )
            if isinstance(items, list):
                for i in items:
                    if isinstance(i, dict) and i.get('deviceInfo'):
                        tmp = i.get('deviceInfo')
                        if isinstance(tmp, dict) and tmp.get('name') == name:
                            result = dict(i)
                            break
        except Exception:
            result = None
        return result

    def get_object_by_id(self, id):
        result = None
        try:
            items = self.dnac.exec(
                family="device_onboarding_pnp",
                function="get_device_by_id",
                params={"id": id}
            )
            if isinstance(items, dict):
                if 'response' in items:
                    items = items.get('response')
            result = result or get_dict_result(items, 'id', id)
        except Exception:
            result = None
        return result

    def exists(self):
        id_exists = False
        name_exists = False
        prev_obj = None
        o_id = self.new_object.get("id")
        name = self.new_object.get("name")
        o_id = o_id or self.new_object.get("_id")
        device_info = self.new_object.get('deviceInfo')
        if device_info and isinstance(device_info, dict) and device_info.get('name'):
            name = name or device_info.get('name')
        if o_id:
            prev_obj = self.get_object_by_id(o_id)
            id_exists = prev_obj is not None and isinstance(prev_obj, dict)
        if not id_exists and name:
            prev_obj = self.get_object_by_name(name)
            name_exists = prev_obj is not None and isinstance(prev_obj, dict)
        if name_exists:
            _id = prev_obj.get("id")
            if id_exists and name_exists and o_id != _id:
                raise InconsistentParameters("The 'id' and 'name' params don't refer to the same object")
            if _id:
                self.new_object.update(dict(id=_id))
            if _id:
                prev_obj = self.get_object_by_id(_id)
        it_exists = prev_obj is not None and isinstance(prev_obj, dict)
        return (it_exists, prev_obj)

    def requires_update(self, current_obj):
        requested_obj = self.new_object

        obj_params = [
            ("_id", "_id"),
            ("deviceInfo", "deviceInfo"),
            ("runSummaryList", "runSummaryList"),
            ("systemResetWorkflow", "systemResetWorkflow"),
            ("systemWorkflow", "systemWorkflow"),
            ("tenantId", "tenantId"),
            ("version", "version"),
            ("workflow", "workflow"),
            ("workflowParameters", "workflowParameters"),
            ("id", "id"),
        ]
        # Method 1. Params present in request (Ansible) obj are the same as the current (DNAC) params
        # If any does not have eq params, it requires update
        return any(not dnac_compare_equality(current_obj.get(dnac_param),
                                             requested_obj.get(ansible_param))
                   for (dnac_param, ansible_param) in obj_params)

    def create(self):
        result = self.dnac.exec(
            family="device_onboarding_pnp",
            function="add_device",
            params=self.create_params(),
            op_modifies=True,
        )
        return result

    def update(self):
        id = self.new_object.get("id")
        name = self.new_object.get("name")
        result = None
        id = id or self.new_object.get("_id")
        device_info = self.new_object.get('deviceInfo')
        if device_info and isinstance(device_info, dict) and device_info.get('name'):
            name = name or device_info.get('name')
        if not id:
            prev_obj_name = self.get_object_by_name(name)
            id_ = None
            if prev_obj_name:
                id_ = prev_obj_name.get("id")
            if id_:
                self.new_object.update(dict(id=id_))
        result = self.dnac.exec(
            family="device_onboarding_pnp",
            function="update_device",
            params=self.update_by_id_params(),
            op_modifies=True,
        )
        return result

    def delete(self):
        id = self.new_object.get("id")
        name = self.new_object.get("name")
        id = id or self.new_object.get("_id")
        device_info = self.new_object.get('deviceInfo')
        if device_info and isinstance(device_info, dict) and device_info.get('name'):
            name = name or device_info.get('name')
        result = None
        if not id:
            prev_obj_name = self.get_object_by_name(name)
            id_ = None
            if prev_obj_name:
                id_ = prev_obj_name.get("id")
            if id_:
                self.new_object.update(dict(id=id_))
        result = self.dnac.exec(
            family="device_onboarding_pnp",
            function="delete_device_by_id_from_pnp",
            params=self.delete_by_id_params(),
        )
        return result


class ActionModule(ActionBase):
    def __init__(self, *args, **kwargs):
        if not ANSIBLE_UTILS_IS_INSTALLED:
            raise AnsibleActionFail("ansible.utils is not installed. Execute 'ansible-galaxy collection install ansible.utils'")
        super(ActionModule, self).__init__(*args, **kwargs)
        self._supports_async = False
        self._supports_check_mode = False
        self._result = None

    # Checks the supplied parameters against the argument spec for this module
    def _check_argspec(self):
        aav = AnsibleArgSpecValidator(
            data=self._task.args,
            schema=dict(argument_spec=argument_spec),
            schema_format="argspec",
            schema_conditionals=dict(
                required_if=required_if,
                required_one_of=required_one_of,
                mutually_exclusive=mutually_exclusive,
                required_together=required_together,
            ),
            name=self._task.action,
        )
        valid, errors, self._task.args = aav.validate()
        if not valid:
            raise AnsibleActionFail(errors)

    def run(self, tmp=None, task_vars=None):
        self._task.diff = False
        self._result = super(ActionModule, self).run(tmp, task_vars)
        self._result["changed"] = False
        self._check_argspec()

        dnac = DNACSDK(self._task.args)
        obj = PnpDevice(self._task.args, dnac)

        state = self._task.args.get("state")

        response = None

        if state == "present":
            (obj_exists, prev_obj) = obj.exists()
            if obj_exists:
                if obj.requires_update(prev_obj):
                    response = obj.update()
                    dnac.object_updated()
                else:
                    response = prev_obj
                    dnac.object_already_present()
            else:
                response = obj.create()
                dnac.object_created()

        elif state == "absent":
            (obj_exists, prev_obj) = obj.exists()
            if obj_exists:
                response = obj.delete()
                dnac.object_deleted()
            else:
                dnac.object_already_absent()

        self._result.update(dict(dnac_response=response))
        self._result.update(dnac.exit_json())
        return self._result
