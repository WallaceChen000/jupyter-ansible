# This code is part of Ansible, but is an independent component.
# This particular file snippet, and this file snippet only, is BSD licensed.
# Modules you write using this snippet, which is embedded dynamically by Ansible
# still belong to the author of the module, and may assign their own license
# to the complete work.
#
# Copyright (c) 2021, Laurent Nicolas <laurentn@netapp.com>
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without modification,
# are permitted provided that the following conditions are met:
#
#    * Redistributions of source code must retain the above copyright
#      notice, this list of conditions and the following disclaimer.
#    * Redistributions in binary form must reproduce the above copyright notice,
#      this list of conditions and the following disclaimer in the documentation
#      and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED.
# IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
# PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE
# USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

""" Support functions for NetApp ansible modules

    Provides common processing for responses and errors from REST calls
"""

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

from ansible_collections.netapp.ontap.plugins.module_utils.rest_generic import get_one_record


def get_vserver(rest_api, name, fields=None):
    api = 'svm/svms'
    query = {'name': name}
    if fields is not None:
        query['fields'] = fields
    vserver, error = get_one_record(rest_api, api, query)
    return vserver, error


def get_vserver_uuid(rest_api, name, module=None, error_on_none=False):
    """ returns a tuple (uuid, error)
        when module is set and an error is found, fails the module and exit
        when error_on_none IS SET, force an error if vserver is not found
    """
    record, error = get_vserver(rest_api, name, 'uuid')
    if error and module:
        module.fail_json(msg="Error fetching vserver %s: %s" % (name, error))
    if not error and record is None and error_on_none:
        error = "vserver %s not found." % name
        if module:
            module.fail_json(msg="Error %s" % error)
    return record['uuid'] if not error and record else None, error
