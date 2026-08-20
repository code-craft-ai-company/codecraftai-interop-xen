"""
    ======================================= CODE GENERATED - DO NOT EDIT =======================================
    This is a code generated execution sequence document, do not manually edit this document.  The 'testbase'
    test framework generates this document in order to layout the test run scopes, parameter creations, and
    test calls in a user ledgible way which is easy to read and also to debug.
"""

__traceback_format_policy__ = "Brief"

import logging

from ccai.xmodules.xlogging.enhancedloggers import getEnhancedLogger

from ccai.testbase.constraints import ConstraintsCatalog

logger = getEnhancedLogger()

constraints_catalog = ConstraintsCatalog()


from ccai.tests.interop.xen.factories import create_xen_transport
from ccai.tests.interop.xen.factories import create_xen_client
from ccai.tests.interop.xen.factories import create_xen_credential
from ccai.tests.interop.xen.factories import create_xen_fast_aspects

def session(sequencer):
    """
    This is the entry point for the test run sequence document.
    """

    with sequencer.enter_session_scope_context() as ssc:


        scope_ccai(sequencer)

    return

def scope_ccai(sequencer):
    """
    This is the entry point for the 'ccai' test scope.
    """

    with sequencer.enter_module_scope_context("ccai") as msc:
        scope_ccai_tests(sequencer)

    return

def scope_ccai_tests(sequencer):
    """
    This is the entry point for the 'ccai_tests' test scope.
    """

    with sequencer.enter_module_scope_context("ccai.tests") as msc:
        scope_ccai_tests_interop(sequencer)

    return

def scope_ccai_tests_interop(sequencer):
    """
    This is the entry point for the 'ccai_tests_interop' test scope.
    """

    with sequencer.enter_module_scope_context("ccai.tests.interop") as msc:
        scope_ccai_tests_interop_xen(sequencer)

    return

def scope_ccai_tests_interop_xen(sequencer):
    """
    This is the entry point for the 'ccai_tests_interop_xen' test scope.
    """

    with sequencer.enter_module_scope_context("ccai.tests.interop.xen") as msc:
        for credential in create_xen_credential():
            for fast_aspects in create_xen_fast_aspects():
                scope_ccai_tests_interop_xen_test_attachments(sequencer, credential, fast_aspects)
                scope_ccai_tests_interop_xen_test_client(sequencer, credential, fast_aspects)
                scope_ccai_tests_interop_xen_test_enumeration(sequencer, credential, fast_aspects)
                scope_ccai_tests_interop_xen_test_properties(sequencer, credential, fast_aspects)
                scope_ccai_tests_interop_xen_test_refresolver(sequencer, credential, fast_aspects)
                scope_ccai_tests_interop_xen_test_session(sequencer, credential, fast_aspects)
                scope_ccai_tests_interop_xen_test_snapshots(sequencer, credential, fast_aspects)
                scope_ccai_tests_interop_xen_test_storage(sequencer, credential, fast_aspects)
                scope_ccai_tests_interop_xen_test_tasks(sequencer, credential, fast_aspects)
                scope_ccai_tests_interop_xen_test_transport(sequencer, credential, fast_aspects)
                scope_ccai_tests_interop_xen_test_vms(sequencer, credential, fast_aspects)

    return

def scope_ccai_tests_interop_xen_test_attachments(sequencer, credential, fast_aspects):
    """
    This is the entry point for the 'ccai_tests_interop_xen_test_attachments' test scope.
    """

    with sequencer.enter_module_scope_context("ccai.tests.interop.xen.test_attachments") as msc:
        # ================ Test Scope: ccai.tests.interop.xen.test_attachments#test_vbd_attach_is_idempotent ================

        test_scope_name = "ccai.tests.interop.xen.test_attachments#test_vbd_attach_is_idempotent"

        with sequencer.enter_test_setup_context(test_scope_name) as tsetup:

            for transport in create_xen_transport():
                for client in create_xen_client(credential ,transport ,fast_aspects):

                    notables = { 'transport': transport, 'client': client }
                    with sequencer.enter_test_scope_context(test_scope_name, notables=notables) as tscope:
                        from ccai.tests.interop.xen.test_attachments import test_vbd_attach_is_idempotent

                        test_vbd_attach_is_idempotent(transport, client, fast_aspects)

        # ================ Test Scope: ccai.tests.interop.xen.test_attachments#test_vbd_attach_returns_typed_record ================

        test_scope_name = "ccai.tests.interop.xen.test_attachments#test_vbd_attach_returns_typed_record"

        with sequencer.enter_test_setup_context(test_scope_name) as tsetup:

            for transport in create_xen_transport():
                for client in create_xen_client(credential ,transport ,fast_aspects):

                    notables = { 'transport': transport, 'client': client }
                    with sequencer.enter_test_scope_context(test_scope_name, notables=notables) as tscope:
                        from ccai.tests.interop.xen.test_attachments import test_vbd_attach_returns_typed_record

                        test_vbd_attach_returns_typed_record(transport, client, fast_aspects)

        # ================ Test Scope: ccai.tests.interop.xen.test_attachments#test_vbd_detach_removes_record ================

        test_scope_name = "ccai.tests.interop.xen.test_attachments#test_vbd_detach_removes_record"

        with sequencer.enter_test_setup_context(test_scope_name) as tsetup:

            for transport in create_xen_transport():
                for client in create_xen_client(credential ,transport ,fast_aspects):

                    notables = { 'transport': transport, 'client': client }
                    with sequencer.enter_test_scope_context(test_scope_name, notables=notables) as tscope:
                        from ccai.tests.interop.xen.test_attachments import test_vbd_detach_removes_record

                        test_vbd_detach_removes_record(transport, client, fast_aspects)

        # ================ Test Scope: ccai.tests.interop.xen.test_attachments#test_vif_attach_is_idempotent ================

        test_scope_name = "ccai.tests.interop.xen.test_attachments#test_vif_attach_is_idempotent"

        with sequencer.enter_test_setup_context(test_scope_name) as tsetup:

            for transport in create_xen_transport():
                for client in create_xen_client(credential ,transport ,fast_aspects):

                    notables = { 'transport': transport, 'client': client }
                    with sequencer.enter_test_scope_context(test_scope_name, notables=notables) as tscope:
                        from ccai.tests.interop.xen.test_attachments import test_vif_attach_is_idempotent

                        test_vif_attach_is_idempotent(transport, client, fast_aspects)

        # ================ Test Scope: ccai.tests.interop.xen.test_attachments#test_vif_attach_returns_typed_record ================

        test_scope_name = "ccai.tests.interop.xen.test_attachments#test_vif_attach_returns_typed_record"

        with sequencer.enter_test_setup_context(test_scope_name) as tsetup:

            for transport in create_xen_transport():
                for client in create_xen_client(credential ,transport ,fast_aspects):

                    notables = { 'transport': transport, 'client': client }
                    with sequencer.enter_test_scope_context(test_scope_name, notables=notables) as tscope:
                        from ccai.tests.interop.xen.test_attachments import test_vif_attach_returns_typed_record

                        test_vif_attach_returns_typed_record(transport, client, fast_aspects)

        # ================ Test Scope: ccai.tests.interop.xen.test_attachments#test_vif_detach_removes_record ================

        test_scope_name = "ccai.tests.interop.xen.test_attachments#test_vif_detach_removes_record"

        with sequencer.enter_test_setup_context(test_scope_name) as tsetup:

            for transport in create_xen_transport():
                for client in create_xen_client(credential ,transport ,fast_aspects):

                    notables = { 'transport': transport, 'client': client }
                    with sequencer.enter_test_scope_context(test_scope_name, notables=notables) as tscope:
                        from ccai.tests.interop.xen.test_attachments import test_vif_detach_removes_record

                        test_vif_detach_removes_record(transport, client, fast_aspects)


    return

def scope_ccai_tests_interop_xen_test_client(sequencer, credential, fast_aspects):
    """
    This is the entry point for the 'ccai_tests_interop_xen_test_client' test scope.
    """

    with sequencer.enter_module_scope_context("ccai.tests.interop.xen.test_client") as msc:
        # ================ Test Scope: ccai.tests.interop.xen.test_client#test_client_exposes_session_manager_and_resolver ================

        test_scope_name = "ccai.tests.interop.xen.test_client#test_client_exposes_session_manager_and_resolver"

        with sequencer.enter_test_setup_context(test_scope_name) as tsetup:

            for transport in create_xen_transport():
                for client in create_xen_client(credential ,transport ,fast_aspects):

                    notables = { 'transport': transport, 'client': client }
                    with sequencer.enter_test_scope_context(test_scope_name, notables=notables) as tscope:
                        from ccai.tests.interop.xen.test_client import test_client_exposes_session_manager_and_resolver

                        test_client_exposes_session_manager_and_resolver(transport, client)

        # ================ Test Scope: ccai.tests.interop.xen.test_client#test_client_group_properties_have_expected_types ================

        test_scope_name = "ccai.tests.interop.xen.test_client#test_client_group_properties_have_expected_types"

        with sequencer.enter_test_setup_context(test_scope_name) as tsetup:

            for transport in create_xen_transport():
                for client in create_xen_client(credential ,transport ,fast_aspects):

                    notables = { 'transport': transport, 'client': client }
                    with sequencer.enter_test_scope_context(test_scope_name, notables=notables) as tscope:
                        from ccai.tests.interop.xen.test_client import test_client_group_properties_have_expected_types

                        test_client_group_properties_have_expected_types(transport, client)

        # ================ Test Scope: ccai.tests.interop.xen.test_client#test_client_groups_are_lazily_constructed_and_cached ================

        test_scope_name = "ccai.tests.interop.xen.test_client#test_client_groups_are_lazily_constructed_and_cached"

        with sequencer.enter_test_setup_context(test_scope_name) as tsetup:

            for transport in create_xen_transport():
                for client in create_xen_client(credential ,transport ,fast_aspects):

                    notables = { 'transport': transport, 'client': client }
                    with sequencer.enter_test_scope_context(test_scope_name, notables=notables) as tscope:
                        from ccai.tests.interop.xen.test_client import test_client_groups_are_lazily_constructed_and_cached

                        test_client_groups_are_lazily_constructed_and_cached(transport, client)

        # ================ Test Scope: ccai.tests.interop.xen.test_client#test_client_groups_share_one_resolver ================

        test_scope_name = "ccai.tests.interop.xen.test_client#test_client_groups_share_one_resolver"

        with sequencer.enter_test_setup_context(test_scope_name) as tsetup:

            for transport in create_xen_transport():
                for client in create_xen_client(credential ,transport ,fast_aspects):

                    notables = { 'transport': transport, 'client': client }
                    with sequencer.enter_test_scope_context(test_scope_name, notables=notables) as tscope:
                        from ccai.tests.interop.xen.test_client import test_client_groups_share_one_resolver

                        test_client_groups_share_one_resolver(transport, client)

        # ================ Test Scope: ccai.tests.interop.xen.test_client#test_client_groups_share_one_session_manager ================

        test_scope_name = "ccai.tests.interop.xen.test_client#test_client_groups_share_one_session_manager"

        with sequencer.enter_test_setup_context(test_scope_name) as tsetup:

            for transport in create_xen_transport():
                for client in create_xen_client(credential ,transport ,fast_aspects):

                    notables = { 'transport': transport, 'client': client }
                    with sequencer.enter_test_scope_context(test_scope_name, notables=notables) as tscope:
                        from ccai.tests.interop.xen.test_client import test_client_groups_share_one_session_manager

                        test_client_groups_share_one_session_manager(transport, client)


    return

def scope_ccai_tests_interop_xen_test_enumeration(sequencer, credential, fast_aspects):
    """
    This is the entry point for the 'ccai_tests_interop_xen_test_enumeration' test scope.
    """

    with sequencer.enter_module_scope_context("ccai.tests.interop.xen.test_enumeration") as msc:
        # ================ Test Scope: ccai.tests.interop.xen.test_enumeration#test_hosts_list_returns_typed_records ================

        test_scope_name = "ccai.tests.interop.xen.test_enumeration#test_hosts_list_returns_typed_records"

        with sequencer.enter_test_setup_context(test_scope_name) as tsetup:

            for transport in create_xen_transport():
                for client in create_xen_client(credential ,transport ,fast_aspects):

                    notables = { 'transport': transport, 'client': client }
                    with sequencer.enter_test_scope_context(test_scope_name, notables=notables) as tscope:
                        from ccai.tests.interop.xen.test_enumeration import test_hosts_list_returns_typed_records

                        test_hosts_list_returns_typed_records(transport, client, fast_aspects)

        # ================ Test Scope: ccai.tests.interop.xen.test_enumeration#test_networks_get_by_name_label_matches ================

        test_scope_name = "ccai.tests.interop.xen.test_enumeration#test_networks_get_by_name_label_matches"

        with sequencer.enter_test_setup_context(test_scope_name) as tsetup:

            for transport in create_xen_transport():
                for client in create_xen_client(credential ,transport ,fast_aspects):

                    notables = { 'transport': transport, 'client': client }
                    with sequencer.enter_test_scope_context(test_scope_name, notables=notables) as tscope:
                        from ccai.tests.interop.xen.test_enumeration import test_networks_get_by_name_label_matches

                        test_networks_get_by_name_label_matches(transport, client, fast_aspects)

        # ================ Test Scope: ccai.tests.interop.xen.test_enumeration#test_networks_list_pifs_excludes_other_hosts ================

        test_scope_name = "ccai.tests.interop.xen.test_enumeration#test_networks_list_pifs_excludes_other_hosts"

        with sequencer.enter_test_setup_context(test_scope_name) as tsetup:

            for transport in create_xen_transport():
                for client in create_xen_client(credential ,transport ,fast_aspects):

                    notables = { 'transport': transport, 'client': client }
                    with sequencer.enter_test_scope_context(test_scope_name, notables=notables) as tscope:
                        from ccai.tests.interop.xen.test_enumeration import test_networks_list_pifs_excludes_other_hosts

                        test_networks_list_pifs_excludes_other_hosts(transport, client, fast_aspects)

        # ================ Test Scope: ccai.tests.interop.xen.test_enumeration#test_networks_list_pifs_filters_by_host ================

        test_scope_name = "ccai.tests.interop.xen.test_enumeration#test_networks_list_pifs_filters_by_host"

        with sequencer.enter_test_setup_context(test_scope_name) as tsetup:

            for transport in create_xen_transport():
                for client in create_xen_client(credential ,transport ,fast_aspects):

                    notables = { 'transport': transport, 'client': client }
                    with sequencer.enter_test_scope_context(test_scope_name, notables=notables) as tscope:
                        from ccai.tests.interop.xen.test_enumeration import test_networks_list_pifs_filters_by_host

                        test_networks_list_pifs_filters_by_host(transport, client, fast_aspects)

        # ================ Test Scope: ccai.tests.interop.xen.test_enumeration#test_networks_list_returns_typed_records ================

        test_scope_name = "ccai.tests.interop.xen.test_enumeration#test_networks_list_returns_typed_records"

        with sequencer.enter_test_setup_context(test_scope_name) as tsetup:

            for transport in create_xen_transport():
                for client in create_xen_client(credential ,transport ,fast_aspects):

                    notables = { 'transport': transport, 'client': client }
                    with sequencer.enter_test_scope_context(test_scope_name, notables=notables) as tscope:
                        from ccai.tests.interop.xen.test_enumeration import test_networks_list_returns_typed_records

                        test_networks_list_returns_typed_records(transport, client, fast_aspects)

        # ================ Test Scope: ccai.tests.interop.xen.test_enumeration#test_pool_get_raises_when_no_pool ================

        test_scope_name = "ccai.tests.interop.xen.test_enumeration#test_pool_get_raises_when_no_pool"

        with sequencer.enter_test_setup_context(test_scope_name) as tsetup:

            for transport in create_xen_transport():
                for client in create_xen_client(credential ,transport ,fast_aspects):

                    notables = { 'transport': transport, 'client': client }
                    with sequencer.enter_test_scope_context(test_scope_name, notables=notables) as tscope:
                        from ccai.tests.interop.xen.test_enumeration import test_pool_get_raises_when_no_pool

                        test_pool_get_raises_when_no_pool(transport, client, fast_aspects)

        # ================ Test Scope: ccai.tests.interop.xen.test_enumeration#test_pool_get_returns_typed_record ================

        test_scope_name = "ccai.tests.interop.xen.test_enumeration#test_pool_get_returns_typed_record"

        with sequencer.enter_test_setup_context(test_scope_name) as tsetup:

            for transport in create_xen_transport():
                for client in create_xen_client(credential ,transport ,fast_aspects):

                    notables = { 'transport': transport, 'client': client }
                    with sequencer.enter_test_scope_context(test_scope_name, notables=notables) as tscope:
                        from ccai.tests.interop.xen.test_enumeration import test_pool_get_returns_typed_record

                        test_pool_get_returns_typed_record(transport, client, fast_aspects)

        # ================ Test Scope: ccai.tests.interop.xen.test_enumeration#test_sr_list_returns_typed_records ================

        test_scope_name = "ccai.tests.interop.xen.test_enumeration#test_sr_list_returns_typed_records"

        with sequencer.enter_test_setup_context(test_scope_name) as tsetup:

            for transport in create_xen_transport():
                for client in create_xen_client(credential ,transport ,fast_aspects):

                    notables = { 'transport': transport, 'client': client }
                    with sequencer.enter_test_scope_context(test_scope_name, notables=notables) as tscope:
                        from ccai.tests.interop.xen.test_enumeration import test_sr_list_returns_typed_records

                        test_sr_list_returns_typed_records(transport, client, fast_aspects)

        # ================ Test Scope: ccai.tests.interop.xen.test_enumeration#test_templates_list_returns_only_templates ================

        test_scope_name = "ccai.tests.interop.xen.test_enumeration#test_templates_list_returns_only_templates"

        with sequencer.enter_test_setup_context(test_scope_name) as tsetup:

            for transport in create_xen_transport():
                for client in create_xen_client(credential ,transport ,fast_aspects):

                    notables = { 'transport': transport, 'client': client }
                    with sequencer.enter_test_scope_context(test_scope_name, notables=notables) as tscope:
                        from ccai.tests.interop.xen.test_enumeration import test_templates_list_returns_only_templates

                        test_templates_list_returns_only_templates(transport, client, fast_aspects)


    return

def scope_ccai_tests_interop_xen_test_properties(sequencer, credential, fast_aspects):
    """
    This is the entry point for the 'ccai_tests_interop_xen_test_properties' test scope.
    """

    with sequencer.enter_module_scope_context("ccai.tests.interop.xen.test_properties") as msc:
        # ================ Test Scope: ccai.tests.interop.xen.test_properties#test_property_handle_wait_succeeds_after_any_pending_count ================

        test_scope_name = "ccai.tests.interop.xen.test_properties#test_property_handle_wait_succeeds_after_any_pending_count"

        with sequencer.enter_test_scope_context(test_scope_name) as tscope:
            from ccai.tests.interop.xen.test_properties import test_property_handle_wait_succeeds_after_any_pending_count

            test_case_name = "ccai.tests.interop.xen.test_properties#test_property_handle_wait_succeeds_after_any_pending_count"

            sequencer.run_property_test(test_property_handle_wait_succeeds_after_any_pending_count, test_case_name, tscope.recorder, tscope.scope_id, {})

        # ================ Test Scope: ccai.tests.interop.xen.test_properties#test_property_record_ref_remembers_uuid_pairs ================

        test_scope_name = "ccai.tests.interop.xen.test_properties#test_property_record_ref_remembers_uuid_pairs"

        with sequencer.enter_test_scope_context(test_scope_name) as tscope:
            from ccai.tests.interop.xen.test_properties import test_property_record_ref_remembers_uuid_pairs

            test_case_name = "ccai.tests.interop.xen.test_properties#test_property_record_ref_remembers_uuid_pairs"

            sequencer.run_property_test(test_property_record_ref_remembers_uuid_pairs, test_case_name, tscope.recorder, tscope.scope_id, {})

        # ================ Test Scope: ccai.tests.interop.xen.test_properties#test_property_relogin_preserves_enumeration_result ================

        test_scope_name = "ccai.tests.interop.xen.test_properties#test_property_relogin_preserves_enumeration_result"

        with sequencer.enter_test_scope_context(test_scope_name) as tscope:
            from ccai.tests.interop.xen.test_properties import test_property_relogin_preserves_enumeration_result

            test_case_name = "ccai.tests.interop.xen.test_properties#test_property_relogin_preserves_enumeration_result"

            sequencer.run_property_test(test_property_relogin_preserves_enumeration_result, test_case_name, tscope.recorder, tscope.scope_id, {})

        # ================ Test Scope: ccai.tests.interop.xen.test_properties#test_property_vdi_create_is_idempotent_under_repetition ================

        test_scope_name = "ccai.tests.interop.xen.test_properties#test_property_vdi_create_is_idempotent_under_repetition"

        with sequencer.enter_test_scope_context(test_scope_name) as tscope:
            from ccai.tests.interop.xen.test_properties import test_property_vdi_create_is_idempotent_under_repetition

            test_case_name = "ccai.tests.interop.xen.test_properties#test_property_vdi_create_is_idempotent_under_repetition"

            sequencer.run_property_test(test_property_vdi_create_is_idempotent_under_repetition, test_case_name, tscope.recorder, tscope.scope_id, {})


    return

def scope_ccai_tests_interop_xen_test_refresolver(sequencer, credential, fast_aspects):
    """
    This is the entry point for the 'ccai_tests_interop_xen_test_refresolver' test scope.
    """

    with sequencer.enter_module_scope_context("ccai.tests.interop.xen.test_refresolver") as msc:
        # ================ Test Scope: ccai.tests.interop.xen.test_refresolver#test_forget_unknown_uuid_is_noop ================

        test_scope_name = "ccai.tests.interop.xen.test_refresolver#test_forget_unknown_uuid_is_noop"

        with sequencer.enter_test_scope_context(test_scope_name) as tscope:
            from ccai.tests.interop.xen.test_refresolver import test_forget_unknown_uuid_is_noop

            test_forget_unknown_uuid_is_noop()

        # ================ Test Scope: ccai.tests.interop.xen.test_refresolver#test_forget_uuid_drops_both_directions ================

        test_scope_name = "ccai.tests.interop.xen.test_refresolver#test_forget_uuid_drops_both_directions"

        with sequencer.enter_test_scope_context(test_scope_name) as tscope:
            from ccai.tests.interop.xen.test_refresolver import test_forget_uuid_drops_both_directions

            test_forget_uuid_drops_both_directions()

        # ================ Test Scope: ccai.tests.interop.xen.test_refresolver#test_maybe_uuid_for_returns_none_when_unknown ================

        test_scope_name = "ccai.tests.interop.xen.test_refresolver#test_maybe_uuid_for_returns_none_when_unknown"

        with sequencer.enter_test_scope_context(test_scope_name) as tscope:
            from ccai.tests.interop.xen.test_refresolver import test_maybe_uuid_for_returns_none_when_unknown

            test_maybe_uuid_for_returns_none_when_unknown()

        # ================ Test Scope: ccai.tests.interop.xen.test_refresolver#test_property_forget_leaves_other_pairs_intact ================

        test_scope_name = "ccai.tests.interop.xen.test_refresolver#test_property_forget_leaves_other_pairs_intact"

        with sequencer.enter_test_scope_context(test_scope_name) as tscope:
            from ccai.tests.interop.xen.test_refresolver import test_property_forget_leaves_other_pairs_intact

            test_case_name = "ccai.tests.interop.xen.test_refresolver#test_property_forget_leaves_other_pairs_intact"

            sequencer.run_property_test(test_property_forget_leaves_other_pairs_intact, test_case_name, tscope.recorder, tscope.scope_id, {})

        # ================ Test Scope: ccai.tests.interop.xen.test_refresolver#test_property_round_trip_is_total_for_remembered_pairs ================

        test_scope_name = "ccai.tests.interop.xen.test_refresolver#test_property_round_trip_is_total_for_remembered_pairs"

        with sequencer.enter_test_scope_context(test_scope_name) as tscope:
            from ccai.tests.interop.xen.test_refresolver import test_property_round_trip_is_total_for_remembered_pairs

            test_case_name = "ccai.tests.interop.xen.test_refresolver#test_property_round_trip_is_total_for_remembered_pairs"

            sequencer.run_property_test(test_property_round_trip_is_total_for_remembered_pairs, test_case_name, tscope.recorder, tscope.scope_id, {})

        # ================ Test Scope: ccai.tests.interop.xen.test_refresolver#test_remember_then_translate_both_directions ================

        test_scope_name = "ccai.tests.interop.xen.test_refresolver#test_remember_then_translate_both_directions"

        with sequencer.enter_test_scope_context(test_scope_name) as tscope:
            from ccai.tests.interop.xen.test_refresolver import test_remember_then_translate_both_directions

            test_remember_then_translate_both_directions()

        # ================ Test Scope: ccai.tests.interop.xen.test_refresolver#test_unknown_ref_raises_semantic_error ================

        test_scope_name = "ccai.tests.interop.xen.test_refresolver#test_unknown_ref_raises_semantic_error"

        with sequencer.enter_test_scope_context(test_scope_name) as tscope:
            from ccai.tests.interop.xen.test_refresolver import test_unknown_ref_raises_semantic_error

            test_unknown_ref_raises_semantic_error()

        # ================ Test Scope: ccai.tests.interop.xen.test_refresolver#test_unknown_uuid_raises_semantic_error ================

        test_scope_name = "ccai.tests.interop.xen.test_refresolver#test_unknown_uuid_raises_semantic_error"

        with sequencer.enter_test_scope_context(test_scope_name) as tscope:
            from ccai.tests.interop.xen.test_refresolver import test_unknown_uuid_raises_semantic_error

            test_unknown_uuid_raises_semantic_error()


    return

def scope_ccai_tests_interop_xen_test_session(sequencer, credential, fast_aspects):
    """
    This is the entry point for the 'ccai_tests_interop_xen_test_session' test scope.
    """

    with sequencer.enter_module_scope_context("ccai.tests.interop.xen.test_session") as msc:
        # ================ Test Scope: ccai.tests.interop.xen.test_session#test_credential_rejects_missing_fields ================

        test_scope_name = "ccai.tests.interop.xen.test_session#test_credential_rejects_missing_fields"

        with sequencer.enter_test_scope_context(test_scope_name) as tscope:
            from ccai.tests.interop.xen.test_session import test_credential_rejects_missing_fields

            test_credential_rejects_missing_fields()

        # ================ Test Scope: ccai.tests.interop.xen.test_session#test_dispatch_lets_semantic_error_bubble ================

        test_scope_name = "ccai.tests.interop.xen.test_session#test_dispatch_lets_semantic_error_bubble"

        with sequencer.enter_test_scope_context(test_scope_name) as tscope:
            from ccai.tests.interop.xen.test_session import test_dispatch_lets_semantic_error_bubble

            test_dispatch_lets_semantic_error_bubble(credential, fast_aspects)

        # ================ Test Scope: ccai.tests.interop.xen.test_session#test_login_caches_session ================

        test_scope_name = "ccai.tests.interop.xen.test_session#test_login_caches_session"

        with sequencer.enter_test_setup_context(test_scope_name) as tsetup:

            for transport in create_xen_transport():
                for client in create_xen_client(credential ,transport ,fast_aspects):

                    notables = { 'transport': transport, 'client': client }
                    with sequencer.enter_test_scope_context(test_scope_name, notables=notables) as tscope:
                        from ccai.tests.interop.xen.test_session import test_login_caches_session

                        test_login_caches_session(transport, client, fast_aspects)

        # ================ Test Scope: ccai.tests.interop.xen.test_session#test_login_failure_raises_authentication_error ================

        test_scope_name = "ccai.tests.interop.xen.test_session#test_login_failure_raises_authentication_error"

        with sequencer.enter_test_scope_context(test_scope_name) as tscope:
            from ccai.tests.interop.xen.test_session import test_login_failure_raises_authentication_error

            test_login_failure_raises_authentication_error(credential, fast_aspects)

        # ================ Test Scope: ccai.tests.interop.xen.test_session#test_logout_releases_session ================

        test_scope_name = "ccai.tests.interop.xen.test_session#test_logout_releases_session"

        with sequencer.enter_test_setup_context(test_scope_name) as tsetup:

            for transport in create_xen_transport():
                for client in create_xen_client(credential ,transport ,fast_aspects):

                    notables = { 'transport': transport, 'client': client }
                    with sequencer.enter_test_scope_context(test_scope_name, notables=notables) as tscope:
                        from ccai.tests.interop.xen.test_session import test_logout_releases_session

                        test_logout_releases_session(transport, client, fast_aspects)

        # ================ Test Scope: ccai.tests.interop.xen.test_session#test_relogin_equivalence_across_first_call ================

        test_scope_name = "ccai.tests.interop.xen.test_session#test_relogin_equivalence_across_first_call"

        with sequencer.enter_test_scope_context(test_scope_name) as tscope:
            from ccai.tests.interop.xen.test_session import test_relogin_equivalence_across_first_call

            test_relogin_equivalence_across_first_call(credential, fast_aspects)

        # ================ Test Scope: ccai.tests.interop.xen.test_session#test_transparent_relogin_on_session_invalid ================

        test_scope_name = "ccai.tests.interop.xen.test_session#test_transparent_relogin_on_session_invalid"

        with sequencer.enter_test_setup_context(test_scope_name) as tsetup:

            for transport in create_xen_transport():
                for client in create_xen_client(credential ,transport ,fast_aspects):

                    notables = { 'transport': transport, 'client': client }
                    with sequencer.enter_test_scope_context(test_scope_name, notables=notables) as tscope:
                        from ccai.tests.interop.xen.test_session import test_transparent_relogin_on_session_invalid

                        test_transparent_relogin_on_session_invalid(transport, client, fast_aspects)


    return

def scope_ccai_tests_interop_xen_test_snapshots(sequencer, credential, fast_aspects):
    """
    This is the entry point for the 'ccai_tests_interop_xen_test_snapshots' test scope.
    """

    with sequencer.enter_module_scope_context("ccai.tests.interop.xen.test_snapshots") as msc:
        # ================ Test Scope: ccai.tests.interop.xen.test_snapshots#test_snapshot_destroy_is_idempotent ================

        test_scope_name = "ccai.tests.interop.xen.test_snapshots#test_snapshot_destroy_is_idempotent"

        with sequencer.enter_test_setup_context(test_scope_name) as tsetup:

            for transport in create_xen_transport():
                for client in create_xen_client(credential ,transport ,fast_aspects):

                    notables = { 'transport': transport, 'client': client }
                    with sequencer.enter_test_scope_context(test_scope_name, notables=notables) as tscope:
                        from ccai.tests.interop.xen.test_snapshots import test_snapshot_destroy_is_idempotent

                        test_snapshot_destroy_is_idempotent(transport, client, fast_aspects)

        # ================ Test Scope: ccai.tests.interop.xen.test_snapshots#test_snapshot_revert ================

        test_scope_name = "ccai.tests.interop.xen.test_snapshots#test_snapshot_revert"

        with sequencer.enter_test_setup_context(test_scope_name) as tsetup:

            for transport in create_xen_transport():
                for client in create_xen_client(credential ,transport ,fast_aspects):

                    notables = { 'transport': transport, 'client': client }
                    with sequencer.enter_test_scope_context(test_scope_name, notables=notables) as tscope:
                        from ccai.tests.interop.xen.test_snapshots import test_snapshot_revert

                        test_snapshot_revert(transport, client, fast_aspects)

        # ================ Test Scope: ccai.tests.interop.xen.test_snapshots#test_snapshot_vm_returns_typed_record ================

        test_scope_name = "ccai.tests.interop.xen.test_snapshots#test_snapshot_vm_returns_typed_record"

        with sequencer.enter_test_setup_context(test_scope_name) as tsetup:

            for transport in create_xen_transport():
                for client in create_xen_client(credential ,transport ,fast_aspects):

                    notables = { 'transport': transport, 'client': client }
                    with sequencer.enter_test_scope_context(test_scope_name, notables=notables) as tscope:
                        from ccai.tests.interop.xen.test_snapshots import test_snapshot_vm_returns_typed_record

                        test_snapshot_vm_returns_typed_record(transport, client, fast_aspects)

        # ================ Test Scope: ccai.tests.interop.xen.test_snapshots#test_snapshots_list_excludes_other_vms ================

        test_scope_name = "ccai.tests.interop.xen.test_snapshots#test_snapshots_list_excludes_other_vms"

        with sequencer.enter_test_setup_context(test_scope_name) as tsetup:

            for transport in create_xen_transport():
                for client in create_xen_client(credential ,transport ,fast_aspects):

                    notables = { 'transport': transport, 'client': client }
                    with sequencer.enter_test_scope_context(test_scope_name, notables=notables) as tscope:
                        from ccai.tests.interop.xen.test_snapshots import test_snapshots_list_excludes_other_vms

                        test_snapshots_list_excludes_other_vms(transport, client, fast_aspects)

        # ================ Test Scope: ccai.tests.interop.xen.test_snapshots#test_snapshots_list_for_vm ================

        test_scope_name = "ccai.tests.interop.xen.test_snapshots#test_snapshots_list_for_vm"

        with sequencer.enter_test_setup_context(test_scope_name) as tsetup:

            for transport in create_xen_transport():
                for client in create_xen_client(credential ,transport ,fast_aspects):

                    notables = { 'transport': transport, 'client': client }
                    with sequencer.enter_test_scope_context(test_scope_name, notables=notables) as tscope:
                        from ccai.tests.interop.xen.test_snapshots import test_snapshots_list_for_vm

                        test_snapshots_list_for_vm(transport, client, fast_aspects)


    return

def scope_ccai_tests_interop_xen_test_storage(sequencer, credential, fast_aspects):
    """
    This is the entry point for the 'ccai_tests_interop_xen_test_storage' test scope.
    """

    with sequencer.enter_module_scope_context("ccai.tests.interop.xen.test_storage") as msc:
        # ================ Test Scope: ccai.tests.interop.xen.test_storage#test_vdi_create_is_idempotent_by_name_label ================

        test_scope_name = "ccai.tests.interop.xen.test_storage#test_vdi_create_is_idempotent_by_name_label"

        with sequencer.enter_test_setup_context(test_scope_name) as tsetup:

            for transport in create_xen_transport():
                for client in create_xen_client(credential ,transport ,fast_aspects):

                    notables = { 'transport': transport, 'client': client }
                    with sequencer.enter_test_scope_context(test_scope_name, notables=notables) as tscope:
                        from ccai.tests.interop.xen.test_storage import test_vdi_create_is_idempotent_by_name_label

                        test_vdi_create_is_idempotent_by_name_label(transport, client, fast_aspects)

        # ================ Test Scope: ccai.tests.interop.xen.test_storage#test_vdi_create_returns_typed_record ================

        test_scope_name = "ccai.tests.interop.xen.test_storage#test_vdi_create_returns_typed_record"

        with sequencer.enter_test_setup_context(test_scope_name) as tsetup:

            for transport in create_xen_transport():
                for client in create_xen_client(credential ,transport ,fast_aspects):

                    notables = { 'transport': transport, 'client': client }
                    with sequencer.enter_test_scope_context(test_scope_name, notables=notables) as tscope:
                        from ccai.tests.interop.xen.test_storage import test_vdi_create_returns_typed_record

                        test_vdi_create_returns_typed_record(transport, client, fast_aspects)

        # ================ Test Scope: ccai.tests.interop.xen.test_storage#test_vdi_delete_is_idempotent ================

        test_scope_name = "ccai.tests.interop.xen.test_storage#test_vdi_delete_is_idempotent"

        with sequencer.enter_test_setup_context(test_scope_name) as tsetup:

            for transport in create_xen_transport():
                for client in create_xen_client(credential ,transport ,fast_aspects):

                    notables = { 'transport': transport, 'client': client }
                    with sequencer.enter_test_scope_context(test_scope_name, notables=notables) as tscope:
                        from ccai.tests.interop.xen.test_storage import test_vdi_delete_is_idempotent

                        test_vdi_delete_is_idempotent(transport, client, fast_aspects)

        # ================ Test Scope: ccai.tests.interop.xen.test_storage#test_vdi_delete_removes_record ================

        test_scope_name = "ccai.tests.interop.xen.test_storage#test_vdi_delete_removes_record"

        with sequencer.enter_test_setup_context(test_scope_name) as tsetup:

            for transport in create_xen_transport():
                for client in create_xen_client(credential ,transport ,fast_aspects):

                    notables = { 'transport': transport, 'client': client }
                    with sequencer.enter_test_scope_context(test_scope_name, notables=notables) as tscope:
                        from ccai.tests.interop.xen.test_storage import test_vdi_delete_removes_record

                        test_vdi_delete_removes_record(transport, client, fast_aspects)

        # ================ Test Scope: ccai.tests.interop.xen.test_storage#test_vdi_delete_unknown_is_noop ================

        test_scope_name = "ccai.tests.interop.xen.test_storage#test_vdi_delete_unknown_is_noop"

        with sequencer.enter_test_setup_context(test_scope_name) as tsetup:

            for transport in create_xen_transport():
                for client in create_xen_client(credential ,transport ,fast_aspects):

                    notables = { 'transport': transport, 'client': client }
                    with sequencer.enter_test_scope_context(test_scope_name, notables=notables) as tscope:
                        from ccai.tests.interop.xen.test_storage import test_vdi_delete_unknown_is_noop

                        test_vdi_delete_unknown_is_noop(transport, client, fast_aspects)

        # ================ Test Scope: ccai.tests.interop.xen.test_storage#test_vdi_list_filters_by_sr ================

        test_scope_name = "ccai.tests.interop.xen.test_storage#test_vdi_list_filters_by_sr"

        with sequencer.enter_test_setup_context(test_scope_name) as tsetup:

            for transport in create_xen_transport():
                for client in create_xen_client(credential ,transport ,fast_aspects):

                    notables = { 'transport': transport, 'client': client }
                    with sequencer.enter_test_scope_context(test_scope_name, notables=notables) as tscope:
                        from ccai.tests.interop.xen.test_storage import test_vdi_list_filters_by_sr

                        test_vdi_list_filters_by_sr(transport, client, fast_aspects)

        # ================ Test Scope: ccai.tests.interop.xen.test_storage#test_vdi_resize_updates_virtual_size ================

        test_scope_name = "ccai.tests.interop.xen.test_storage#test_vdi_resize_updates_virtual_size"

        with sequencer.enter_test_setup_context(test_scope_name) as tsetup:

            for transport in create_xen_transport():
                for client in create_xen_client(credential ,transport ,fast_aspects):

                    notables = { 'transport': transport, 'client': client }
                    with sequencer.enter_test_scope_context(test_scope_name, notables=notables) as tscope:
                        from ccai.tests.interop.xen.test_storage import test_vdi_resize_updates_virtual_size

                        test_vdi_resize_updates_virtual_size(transport, client, fast_aspects)


    return

def scope_ccai_tests_interop_xen_test_tasks(sequencer, credential, fast_aspects):
    """
    This is the entry point for the 'ccai_tests_interop_xen_test_tasks' test scope.
    """

    with sequencer.enter_module_scope_context("ccai.tests.interop.xen.test_tasks") as msc:
        # ================ Test Scope: ccai.tests.interop.xen.test_tasks#test_handle_cancel_invokes_canceller ================

        test_scope_name = "ccai.tests.interop.xen.test_tasks#test_handle_cancel_invokes_canceller"

        with sequencer.enter_test_scope_context(test_scope_name) as tscope:
            from ccai.tests.interop.xen.test_tasks import test_handle_cancel_invokes_canceller

            test_handle_cancel_invokes_canceller()

        # ================ Test Scope: ccai.tests.interop.xen.test_tasks#test_handle_cancel_terminal_is_noop ================

        test_scope_name = "ccai.tests.interop.xen.test_tasks#test_handle_cancel_terminal_is_noop"

        with sequencer.enter_test_scope_context(test_scope_name) as tscope:
            from ccai.tests.interop.xen.test_tasks import test_handle_cancel_terminal_is_noop

            test_handle_cancel_terminal_is_noop()

        # ================ Test Scope: ccai.tests.interop.xen.test_tasks#test_handle_cancel_without_canceller_raises ================

        test_scope_name = "ccai.tests.interop.xen.test_tasks#test_handle_cancel_without_canceller_raises"

        with sequencer.enter_test_scope_context(test_scope_name) as tscope:
            from ccai.tests.interop.xen.test_tasks import test_handle_cancel_without_canceller_raises

            test_handle_cancel_without_canceller_raises()

        # ================ Test Scope: ccai.tests.interop.xen.test_tasks#test_handle_wait_cancelled ================

        test_scope_name = "ccai.tests.interop.xen.test_tasks#test_handle_wait_cancelled"

        with sequencer.enter_test_scope_context(test_scope_name) as tscope:
            from ccai.tests.interop.xen.test_tasks import test_handle_wait_cancelled

            test_handle_wait_cancelled()

        # ================ Test Scope: ccai.tests.interop.xen.test_tasks#test_handle_wait_failure_raises ================

        test_scope_name = "ccai.tests.interop.xen.test_tasks#test_handle_wait_failure_raises"

        with sequencer.enter_test_scope_context(test_scope_name) as tscope:
            from ccai.tests.interop.xen.test_tasks import test_handle_wait_failure_raises

            test_handle_wait_failure_raises()

        # ================ Test Scope: ccai.tests.interop.xen.test_tasks#test_handle_wait_success ================

        test_scope_name = "ccai.tests.interop.xen.test_tasks#test_handle_wait_success"

        with sequencer.enter_test_scope_context(test_scope_name) as tscope:
            from ccai.tests.interop.xen.test_tasks import test_handle_wait_success

            test_handle_wait_success()

        # ================ Test Scope: ccai.tests.interop.xen.test_tasks#test_handle_wait_times_out ================

        test_scope_name = "ccai.tests.interop.xen.test_tasks#test_handle_wait_times_out"

        with sequencer.enter_test_scope_context(test_scope_name) as tscope:
            from ccai.tests.interop.xen.test_tasks import test_handle_wait_times_out

            test_handle_wait_times_out()

        # ================ Test Scope: ccai.tests.interop.xen.test_tasks#test_task_status_terminal_classification ================

        test_scope_name = "ccai.tests.interop.xen.test_tasks#test_task_status_terminal_classification"

        with sequencer.enter_test_scope_context(test_scope_name) as tscope:
            from ccai.tests.interop.xen.test_tasks import test_task_status_terminal_classification

            test_task_status_terminal_classification()

        # ================ Test Scope: ccai.tests.interop.xen.test_tasks#test_tasks_get_status_returns_typed_snapshot ================

        test_scope_name = "ccai.tests.interop.xen.test_tasks#test_tasks_get_status_returns_typed_snapshot"

        with sequencer.enter_test_setup_context(test_scope_name) as tsetup:

            for transport in create_xen_transport():
                for client in create_xen_client(credential ,transport ,fast_aspects):

                    notables = { 'transport': transport, 'client': client }
                    with sequencer.enter_test_scope_context(test_scope_name, notables=notables) as tscope:
                        from ccai.tests.interop.xen.test_tasks import test_tasks_get_status_returns_typed_snapshot

                        test_tasks_get_status_returns_typed_snapshot(transport, client, fast_aspects)

        # ================ Test Scope: ccai.tests.interop.xen.test_tasks#test_xentaskhandle_conforms_to_itaskhandle ================

        test_scope_name = "ccai.tests.interop.xen.test_tasks#test_xentaskhandle_conforms_to_itaskhandle"

        with sequencer.enter_test_scope_context(test_scope_name) as tscope:
            from ccai.tests.interop.xen.test_tasks import test_xentaskhandle_conforms_to_itaskhandle

            test_xentaskhandle_conforms_to_itaskhandle()


    return

def scope_ccai_tests_interop_xen_test_transport(sequencer, credential, fast_aspects):
    """
    This is the entry point for the 'ccai_tests_interop_xen_test_transport' test scope.
    """

    with sequencer.enter_module_scope_context("ccai.tests.interop.xen.test_transport") as msc:
        # ================ Test Scope: ccai.tests.interop.xen.test_transport#test_dispatch_logs_in_before_first_call ================

        test_scope_name = "ccai.tests.interop.xen.test_transport#test_dispatch_logs_in_before_first_call"

        with sequencer.enter_test_setup_context(test_scope_name) as tsetup:

            for transport in create_xen_transport():
                for client in create_xen_client(credential ,transport ,fast_aspects):

                    notables = { 'transport': transport, 'client': client }
                    with sequencer.enter_test_scope_context(test_scope_name, notables=notables) as tscope:
                        from ccai.tests.interop.xen.test_transport import test_dispatch_logs_in_before_first_call

                        test_dispatch_logs_in_before_first_call(transport, client, fast_aspects)

        # ================ Test Scope: ccai.tests.interop.xen.test_transport#test_dispatch_unknown_method_raises_xen_error ================

        test_scope_name = "ccai.tests.interop.xen.test_transport#test_dispatch_unknown_method_raises_xen_error"

        with sequencer.enter_test_setup_context(test_scope_name) as tsetup:

            for transport in create_xen_transport():
                for client in create_xen_client(credential ,transport ,fast_aspects):

                    notables = { 'transport': transport, 'client': client }
                    with sequencer.enter_test_scope_context(test_scope_name, notables=notables) as tscope:
                        from ccai.tests.interop.xen.test_transport import test_dispatch_unknown_method_raises_xen_error

                        test_dispatch_unknown_method_raises_xen_error(transport, client, fast_aspects)

        # ================ Test Scope: ccai.tests.interop.xen.test_transport#test_is_session_invalid_detects_marker ================

        test_scope_name = "ccai.tests.interop.xen.test_transport#test_is_session_invalid_detects_marker"

        with sequencer.enter_test_scope_context(test_scope_name) as tscope:
            from ccai.tests.interop.xen.test_transport import test_is_session_invalid_detects_marker

            test_is_session_invalid_detects_marker()

        # ================ Test Scope: ccai.tests.interop.xen.test_transport#test_session_manager_requires_credential ================

        test_scope_name = "ccai.tests.interop.xen.test_transport#test_session_manager_requires_credential"

        with sequencer.enter_test_scope_context(test_scope_name) as tscope:
            from ccai.tests.interop.xen.test_transport import test_session_manager_requires_credential

            test_session_manager_requires_credential()

        # ================ Test Scope: ccai.tests.interop.xen.test_transport#test_unwrap_auth_failure_raises_authentication_error ================

        test_scope_name = "ccai.tests.interop.xen.test_transport#test_unwrap_auth_failure_raises_authentication_error"

        with sequencer.enter_test_scope_context(test_scope_name) as tscope:
            from ccai.tests.interop.xen.test_transport import test_unwrap_auth_failure_raises_authentication_error

            test_unwrap_auth_failure_raises_authentication_error()

        # ================ Test Scope: ccai.tests.interop.xen.test_transport#test_unwrap_failure_raises_xen_error ================

        test_scope_name = "ccai.tests.interop.xen.test_transport#test_unwrap_failure_raises_xen_error"

        with sequencer.enter_test_scope_context(test_scope_name) as tscope:
            from ccai.tests.interop.xen.test_transport import test_unwrap_failure_raises_xen_error

            test_unwrap_failure_raises_xen_error()

        # ================ Test Scope: ccai.tests.interop.xen.test_transport#test_unwrap_returns_bare_value ================

        test_scope_name = "ccai.tests.interop.xen.test_transport#test_unwrap_returns_bare_value"

        with sequencer.enter_test_scope_context(test_scope_name) as tscope:
            from ccai.tests.interop.xen.test_transport import test_unwrap_returns_bare_value

            test_unwrap_returns_bare_value()

        # ================ Test Scope: ccai.tests.interop.xen.test_transport#test_unwrap_success_returns_value ================

        test_scope_name = "ccai.tests.interop.xen.test_transport#test_unwrap_success_returns_value"

        with sequencer.enter_test_scope_context(test_scope_name) as tscope:
            from ccai.tests.interop.xen.test_transport import test_unwrap_success_returns_value

            test_unwrap_success_returns_value()


    return

def scope_ccai_tests_interop_xen_test_vms(sequencer, credential, fast_aspects):
    """
    This is the entry point for the 'ccai_tests_interop_xen_test_vms' test scope.
    """

    with sequencer.enter_module_scope_context("ccai.tests.interop.xen.test_vms") as msc:
        # ================ Test Scope: ccai.tests.interop.xen.test_vms#test_clone_applies_overrides ================

        test_scope_name = "ccai.tests.interop.xen.test_vms#test_clone_applies_overrides"

        with sequencer.enter_test_setup_context(test_scope_name) as tsetup:

            for transport in create_xen_transport():
                for client in create_xen_client(credential ,transport ,fast_aspects):

                    notables = { 'transport': transport, 'client': client }
                    with sequencer.enter_test_scope_context(test_scope_name, notables=notables) as tscope:
                        from ccai.tests.interop.xen.test_vms import test_clone_applies_overrides

                        test_clone_applies_overrides(transport, client, fast_aspects)

        # ================ Test Scope: ccai.tests.interop.xen.test_vms#test_clone_from_template_returns_vm_and_handle ================

        test_scope_name = "ccai.tests.interop.xen.test_vms#test_clone_from_template_returns_vm_and_handle"

        with sequencer.enter_test_setup_context(test_scope_name) as tsetup:

            for transport in create_xen_transport():
                for client in create_xen_client(credential ,transport ,fast_aspects):

                    notables = { 'transport': transport, 'client': client }
                    with sequencer.enter_test_scope_context(test_scope_name, notables=notables) as tscope:
                        from ccai.tests.interop.xen.test_vms import test_clone_from_template_returns_vm_and_handle

                        test_clone_from_template_returns_vm_and_handle(transport, client, fast_aspects)

        # ================ Test Scope: ccai.tests.interop.xen.test_vms#test_clone_is_idempotent_by_name_label ================

        test_scope_name = "ccai.tests.interop.xen.test_vms#test_clone_is_idempotent_by_name_label"

        with sequencer.enter_test_setup_context(test_scope_name) as tsetup:

            for transport in create_xen_transport():
                for client in create_xen_client(credential ,transport ,fast_aspects):

                    notables = { 'transport': transport, 'client': client }
                    with sequencer.enter_test_scope_context(test_scope_name, notables=notables) as tscope:
                        from ccai.tests.interop.xen.test_vms import test_clone_is_idempotent_by_name_label

                        test_clone_is_idempotent_by_name_label(transport, client, fast_aspects)

        # ================ Test Scope: ccai.tests.interop.xen.test_vms#test_provision_task_handle_completes ================

        test_scope_name = "ccai.tests.interop.xen.test_vms#test_provision_task_handle_completes"

        with sequencer.enter_test_setup_context(test_scope_name) as tsetup:

            for transport in create_xen_transport():
                for client in create_xen_client(credential ,transport ,fast_aspects):

                    notables = { 'transport': transport, 'client': client }
                    with sequencer.enter_test_scope_context(test_scope_name, notables=notables) as tscope:
                        from ccai.tests.interop.xen.test_vms import test_provision_task_handle_completes

                        test_provision_task_handle_completes(transport, client, fast_aspects)

        # ================ Test Scope: ccai.tests.interop.xen.test_vms#test_vm_destroy_is_idempotent ================

        test_scope_name = "ccai.tests.interop.xen.test_vms#test_vm_destroy_is_idempotent"

        with sequencer.enter_test_setup_context(test_scope_name) as tsetup:

            for transport in create_xen_transport():
                for client in create_xen_client(credential ,transport ,fast_aspects):

                    notables = { 'transport': transport, 'client': client }
                    with sequencer.enter_test_scope_context(test_scope_name, notables=notables) as tscope:
                        from ccai.tests.interop.xen.test_vms import test_vm_destroy_is_idempotent

                        test_vm_destroy_is_idempotent(transport, client, fast_aspects)

        # ================ Test Scope: ccai.tests.interop.xen.test_vms#test_vm_destroy_removes_record ================

        test_scope_name = "ccai.tests.interop.xen.test_vms#test_vm_destroy_removes_record"

        with sequencer.enter_test_setup_context(test_scope_name) as tsetup:

            for transport in create_xen_transport():
                for client in create_xen_client(credential ,transport ,fast_aspects):

                    notables = { 'transport': transport, 'client': client }
                    with sequencer.enter_test_scope_context(test_scope_name, notables=notables) as tscope:
                        from ccai.tests.interop.xen.test_vms import test_vm_destroy_removes_record

                        test_vm_destroy_removes_record(transport, client, fast_aspects)

        # ================ Test Scope: ccai.tests.interop.xen.test_vms#test_vm_power_operations ================

        test_scope_name = "ccai.tests.interop.xen.test_vms#test_vm_power_operations"

        with sequencer.enter_test_setup_context(test_scope_name) as tsetup:

            for transport in create_xen_transport():
                for client in create_xen_client(credential ,transport ,fast_aspects):

                    notables = { 'transport': transport, 'client': client }
                    with sequencer.enter_test_scope_context(test_scope_name, notables=notables) as tscope:
                        from ccai.tests.interop.xen.test_vms import test_vm_power_operations

                        test_vm_power_operations(transport, client, fast_aspects)

        # ================ Test Scope: ccai.tests.interop.xen.test_vms#test_vm_wait_for_power_state ================

        test_scope_name = "ccai.tests.interop.xen.test_vms#test_vm_wait_for_power_state"

        with sequencer.enter_test_setup_context(test_scope_name) as tsetup:

            for transport in create_xen_transport():
                for client in create_xen_client(credential ,transport ,fast_aspects):

                    notables = { 'transport': transport, 'client': client }
                    with sequencer.enter_test_scope_context(test_scope_name, notables=notables) as tscope:
                        from ccai.tests.interop.xen.test_vms import test_vm_wait_for_power_state

                        test_vm_wait_for_power_state(transport, client, fast_aspects)

        # ================ Test Scope: ccai.tests.interop.xen.test_vms#test_vms_get_by_name_label ================

        test_scope_name = "ccai.tests.interop.xen.test_vms#test_vms_get_by_name_label"

        with sequencer.enter_test_setup_context(test_scope_name) as tsetup:

            for transport in create_xen_transport():
                for client in create_xen_client(credential ,transport ,fast_aspects):

                    notables = { 'transport': transport, 'client': client }
                    with sequencer.enter_test_scope_context(test_scope_name, notables=notables) as tscope:
                        from ccai.tests.interop.xen.test_vms import test_vms_get_by_name_label

                        test_vms_get_by_name_label(transport, client, fast_aspects)

        # ================ Test Scope: ccai.tests.interop.xen.test_vms#test_vms_get_by_uuid ================

        test_scope_name = "ccai.tests.interop.xen.test_vms#test_vms_get_by_uuid"

        with sequencer.enter_test_setup_context(test_scope_name) as tsetup:

            for transport in create_xen_transport():
                for client in create_xen_client(credential ,transport ,fast_aspects):

                    notables = { 'transport': transport, 'client': client }
                    with sequencer.enter_test_scope_context(test_scope_name, notables=notables) as tscope:
                        from ccai.tests.interop.xen.test_vms import test_vms_get_by_uuid

                        test_vms_get_by_uuid(transport, client, fast_aspects)

        # ================ Test Scope: ccai.tests.interop.xen.test_vms#test_vms_list_excludes_templates ================

        test_scope_name = "ccai.tests.interop.xen.test_vms#test_vms_list_excludes_templates"

        with sequencer.enter_test_setup_context(test_scope_name) as tsetup:

            for transport in create_xen_transport():
                for client in create_xen_client(credential ,transport ,fast_aspects):

                    notables = { 'transport': transport, 'client': client }
                    with sequencer.enter_test_scope_context(test_scope_name, notables=notables) as tscope:
                        from ccai.tests.interop.xen.test_vms import test_vms_list_excludes_templates

                        test_vms_list_excludes_templates(transport, client, fast_aspects)


    return
