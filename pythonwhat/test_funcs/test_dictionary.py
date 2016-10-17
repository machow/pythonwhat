from pythonwhat.State import State
from pythonwhat.Reporter import Reporter
from pythonwhat.Test import DefinedProcessTest, InstanceProcessTest, DefinedCollProcessTest, EqualValueProcessTest
from pythonwhat.Feedback import Feedback
from pythonwhat.tasks import isDefinedInProcess, isInstanceInProcess, getKeysInProcess, getValueInProcess, ReprFail
from .test_object import check_object

def test_dictionary(name,
                    keys=None,
                    undefined_msg=None,
                    not_dictionary_msg=None,
                    key_missing_msg=None,
                    incorrect_value_msg=None,
                    state=None):
    """Test the contents of a dictionary.
    """

    rep = Reporter.active_reporter
    rep.set_tag("fun", "test_dictionary")

    sol_keys = check_dict(name, undefined_msg, not_dictionary_msg, state=state)

    # set keys or check if manual keys are valid
    if not keys: keys = sol_keys

    for key in keys:
        # check if key in dictionary
        test_key(name, key, incorrect_value_msg, key_missing_msg, sol_keys, state=state)


def check_dict(name, undefined_msg, not_dictionary_msg, state=None):
    rep = Reporter.active_reporter

    # Check if defined
    if not undefined_msg:
        undefined_msg = "Are you sure you defined the dictionary `%s`?" % name

    # check but don't get solution dict representation
    state = check_object(name, undefined_msg, state=state)

    is_dict(name, not_dictionary_msg, state=state)

    sol_keys = getKeysInProcess(name, state.solution_process)
    if sol_keys is None:
        raise ValueError("Something went wrong in figuring out the keys for %s in the solution process" % name)

    return sol_keys

def is_dict(name, not_dictionary_msg, state=None):
    rep = Reporter.active_reporter

    if not isInstanceInProcess(name, state.solution_object, state.solution_process):
        raise ValueError("%r is not a dictionary in the solution environment" % name)

    if not not_dictionary_msg:
        not_dictionary_msg = "`%s` is not a dictionary." % name
    rep.do_test(InstanceProcessTest(name, dict, state.student_process, Feedback(not_dictionary_msg)))

def has_key(name, key, key_missing_msg, sol_keys=None, state=None):
    rep = Reporter.active_reporter

    if not sol_keys:
        getKeysInProcess(name, state.solution_process)

    if key not in set(sol_keys):
        raise NameError("Not all keys you specified are actually keys in %s in the solution process" % name)

    # check if key available
    if not key_missing_msg:
        msg = "Have you specified a key `%s` inside `%s`?" % (str(key), name)
    else:
        msg = key_missing_msg
    rep.do_test(DefinedCollProcessTest(name, key, state.student_process, Feedback(msg)))

def test_key(name, key, incorrect_value_msg, key_missing_msg, sol_keys=None, state=None):
    rep = Reporter.active_reporter

    has_key(name, key, key_missing_msg, sol_keys, state=state)

    sol_value = getValueInProcess(name, key, state.solution_process)
    if isinstance(sol_value, ReprFail):
        raise NameError("Value from %r can't be fetched from the solution process: %s" % c(name, sol_value.info))

    # check if value ok
    msg = incorrect_value_msg or \
          "Have you specified the correct value for the key `%s` inside `%s`?" % (str(key), name)

    rep.do_test(EqualValueProcessTest(name, key, state.student_process, sol_value, Feedback(msg)))
