# -*- coding: utf-8 -*- #
# Copyright 2017 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""A library to build a test results summary."""

from __future__ import absolute_import
from __future__ import division
from __future__ import unicode_literals

import collections

from apitools.base.py import exceptions as apitools_exceptions

from googlecloudsdk.api_lib.firebase.test import util
from googlecloudsdk.calliope import exceptions
from googlecloudsdk.core import log


_NATIVE_CRASH = 'Native crash'
_NATIVE_CRASH_DETAILED_FORMAT = '''\
For test execution [{0}], a native process crashed on the device. This could \
be caused by your app, by an app dependency, or by an unrelated cause.'''
_INFRASTRUCTURE_FAILURE = 'Infrastructure failure'
_INFRASTRUCTURE_FAILURE_DETAILED_FORMAT = '''\
Need help for test execution [{0}]? Please join the #test-lab Slack channel \
at https://firebase.community/ and include execution ID [{1}] with your \
question.'''


class TestOutcome(collections.namedtuple(
    'TestOutcome', ['outcome', 'axis_value', 'test_details'])):
  """A tuple to hold the outcome for a single test axis value.

  Fields:
    outcome: string containing the test outcome (e.g. 'Passed')
    axis_value: string representing one axis value within the matrix.
    test_details: string with extra details (e.g. "Incompatible architecture")
  """


class FlakyAttemptsTestOutcome(
    collections.namedtuple('TestOutcome',
                           ['outcome', 'axis_value', 'passed_executions'])):
  """A tuple to hold the outcome for a single test axis value with flaky reruns.

  Fields:
    outcome: string containing the test outcome (e.g. 'Passed')
    axis_value: string representing one axis value within the matrix.
    passed_executions: string with number of passed attempts out of total number
  """


# Human-freindly test outcome names
_SUCCESS = 'Passed'
_FLAKY = 'Flaky'
_FAILURE = 'Failed'
_SKIPPED = 'Skipped'
_INCONCLUSIVE = 'Inconclusive'

# Relative sort weightings for test outcomes
_OUTCOME_SORTING = {
    _FAILURE: 10,
    _FLAKY: 20,
    _SUCCESS: 30,
    _INCONCLUSIVE: 40,
    _SKIPPED: 50,
}


def _TestOutcomeSortKey(x):
  """Transform a TestOutcome to a tuple yielding the desired sort order."""
  return tuple([_OUTCOME_SORTING[x.outcome], x.test_details, x.axis_value])


def _FlakyAttemptsTestOutcomeSortKey(x):
  """Transform a TestOutcome to a tuple yielding the desired sort order."""
  return tuple([_OUTCOME_SORTING[x.outcome], x.passed_executions, x.axis_value])


class ToolResultsSummaryFetcher(object):
  """Creates Test Results summary using data from the Tool Results API.
  """

  def __init__(self, project, client, messages, tool_results_ids):
    """Constructs a ToolResultsSummaryFetcher.

    Args:
      project: string containing the GCE project id.
      client: ToolResults API client lib generated by apitools.
      messages: ToolResults API message classes generated by apitools.
      tool_results_ids: a ToolResultsIds object holding history & execution IDs.
    """
    self._project = project
    self._client = client
    self._messages = messages
    self._history_id = tool_results_ids.history_id
    self._execution_id = tool_results_ids.execution_id
    self._outcome_names = {
        messages.Outcome.SummaryValueValuesEnum.success: _SUCCESS,
        messages.Outcome.SummaryValueValuesEnum.failure: _FAILURE,
        messages.Outcome.SummaryValueValuesEnum.skipped: _SKIPPED,
        messages.Outcome.SummaryValueValuesEnum.inconclusive: _INCONCLUSIVE,
        messages.PrimaryStep.RollUpValueValuesEnum.success: _SUCCESS,
        messages.PrimaryStep.RollUpValueValuesEnum.flaky: _FLAKY,
        messages.PrimaryStep.RollUpValueValuesEnum.failure: _FAILURE,
        messages.PrimaryStep.RollUpValueValuesEnum.skipped: _SKIPPED,
        messages.PrimaryStep.RollUpValueValuesEnum.inconclusive: _INCONCLUSIVE,
    }

  def FetchMatrixRollupOutcome(self):
    """Gets a test execution's rolled-up outcome from the Tool Results service.

    Returns:
      The rolled-up test execution outcome (type: toolresults_v1beta3.Outcome).

    Raises:
      HttpException if the Tool Results service reports a back-end error.
    """
    request = self._messages.ToolresultsProjectsHistoriesExecutionsGetRequest(
        projectId=self._project,
        historyId=self._history_id,
        executionId=self._execution_id)
    try:
      response = self._client.projects_histories_executions.Get(request)
      log.debug('\nTRHistoriesExecutions.Get response:\n{0}\n'.format(response))
      return response.outcome
    except apitools_exceptions.HttpError as error:
      msg = 'Http error fetching test roll-up outcome: ' + util.GetError(error)
      raise exceptions.HttpException(msg)

  def CreateMatrixOutcomeSummary(self):
    """Fetches test results and creates a test outcome summary.

    Lists all the steps in an execution and creates a high-level outcome summary
    for each step (pass/fail/inconclusive). Each step represents a combination
    of a test execution (e.g. running the tests on a Nexus 5 in portrait mode
    using the en locale and API level 18).

    Returns:
      A list of TestOutcome objects.

    Raises:
      HttpException if the Tool Results service reports a back-end error.
    """
    outcomes = []
    steps = self._ListAllSteps()
    if not steps:
      log.warning(
          'No results found, something went wrong. Try re-running the tests.')
      return outcomes

    for step in steps:
      axis_value = self._GetAxisValue(step)
      # It's a bug in Tool Results if we get no outcome, but this guard
      # prevents a stack trace if it should happen.
      if not step.outcome:
        log.warning('Step for [{0}] had no outcome value.'.format(axis_value))
      else:
        details = self._GetStepOutcomeDetails(step)
        if _NATIVE_CRASH in details:
          log.warning(_NATIVE_CRASH_DETAILED_FORMAT.format(axis_value))
        if _INFRASTRUCTURE_FAILURE in details:
          log.warning(
              _INFRASTRUCTURE_FAILURE_DETAILED_FORMAT.format(
                  axis_value, self._execution_id))
        outcome_str = self._GetOutcomeSummaryDisplayName(step.outcome.summary)
        outcomes.append(
            TestOutcome(outcome=outcome_str,
                        axis_value=axis_value,
                        test_details=details))

    return sorted(outcomes, key=_TestOutcomeSortKey)

  def CreateFlakyAttemptsMatrixOutcomeSummary(self):
    """Fetches test results and creates a test outcome summary.

    Lists all the primary steps in an execution and creates a high-level rollup
    outcome summary for each group of steps (pass/flaky/fail/inconclusive). Each
    primary step represents a combination of a test execution (e.g. running the
    tests on a Nexus 5 in portrait mode using the en locale and API level 18).

    Returns:
      A list of TestOutcome objects.

    Raises:
      HttpException if the Tool Results service reports a back-end error.
    """
    outcomes = []
    steps = self._ListAllSteps()
    if not steps:
      log.warning(
          'No results found, something went wrong. Try re-running the tests.')
      return outcomes

    summary_enum = self._messages.Outcome.SummaryValueValuesEnum
    pass_counter = collections.Counter()
    total_counter = collections.Counter()
    for step in steps:
      axis_value = self._GetAxisValue(step)
      total_counter[axis_value] += 1
      if step.outcome and step.outcome.summary == summary_enum.success:
        pass_counter[axis_value] += 1

    for step in steps:
      # It's a bug in Tool Results if we get no outcome, but this guard
      # prevents a stack trace if it should happen.
      if not step.outcome:
        log.warning('Step for [{0}] had no outcome value.'.format(axis_value))
      elif not step.multiStep or step.multiStep.multistepNumber < 1:
        axis_value = self._GetAxisValue(step)
        pass_ratio = pass_counter[axis_value] / total_counter[axis_value]
        passed_str = '{:.0%} ({p} of {t})'.format(
            pass_ratio, p=pass_counter[axis_value], t=total_counter[axis_value])
        outcome_str = self._GetOutcomeSummaryDisplayName(
            step.multiStep.primaryStep.rollUp if step.multiStep.primaryStep
            else step.outcome.summary)
        outcomes.append(
            FlakyAttemptsTestOutcome(
                outcome=outcome_str,
                axis_value=axis_value,
                passed_executions=passed_str))

    return sorted(outcomes, key=_FlakyAttemptsTestOutcomeSortKey)

  def _GetAxisValue(self, step):
    axes = {}
    for dimension in step.dimensionValue:
      axes[dimension.key] = dimension.value
    return ('{m}-{v}-{l}-{o}'.format(
        m=axes.get('Model', '?'),
        v=axes.get('Version', '?'),
        l=axes.get('Locale', '?'),
        o=axes.get('Orientation', '?')))

  def _ListAllSteps(self):
    """Lists all steps for a test execution using the Tool Results service.

    Returns:
      The full list of steps for a test execution.
    """
    response = self._ListSteps(None)
    steps = []
    steps.extend(response.steps)

    while response.nextPageToken:
      response = self._ListSteps(response.nextPageToken)
      steps.extend(response.steps)

    return steps

  def _ListSteps(self, page_token):
    """Lists one page of steps using the Tool Results service.

    Args:
      page_token: A page token to attach to the List request.

    Returns:
      A ListStepsResponse containing a single page's steps.

    Raises:
      HttpException if the Tool Results service reports a back-end error.
    """
    request = (
        self._messages.ToolresultsProjectsHistoriesExecutionsStepsListRequest(
            projectId=self._project, historyId=self._history_id,
            executionId=self._execution_id, pageSize=100, pageToken=page_token))
    try:
      response = self._client.projects_histories_executions_steps.List(request)
      log.debug('\nToolResultsSteps.List response:\n{0}\n'.format(response))
      return response
    except apitools_exceptions.HttpError as error:
      msg = 'Http error while listing test results: ' +  util.GetError(error)
      raise exceptions.HttpException(msg)

  def _GetOutcomeSummaryDisplayName(self, outcome):
    """Transforms the outcome enum to a human readable outcome.

    Args:
      outcome: An Outcome.SummaryValueValuesEnum value.

    Returns:
      A string containing a human readable outcome.
    """
    try:
      return self._outcome_names[outcome]
    except ValueError:
      return 'Unknown'

  def _GetStepOutcomeDetails(self, step):
    """Turn test outcome counts and details into something human readable."""
    outcome = step.outcome
    summary_enum = self._messages.Outcome.SummaryValueValuesEnum

    if outcome.summary == summary_enum.success:
      total = 0
      for overview in step.testExecutionStep.testSuiteOverviews:
        total += overview.totalCount or 0
      details = '{t} test cases passed'.format(t=total) if total else '--'

      if outcome.successDetail and outcome.successDetail.otherNativeCrash:
        return '{d} ({c})'.format(d=details, c=_NATIVE_CRASH)
      else:
        return details

    elif outcome.summary == summary_enum.failure:
      if outcome.failureDetail:
        details = ''
        # Note: crashed/timedOut/notInstalled flags are mutually exclusive
        if outcome.failureDetail.crashed:
          details = 'Application crashed'
        elif outcome.failureDetail.timedOut:
          details = 'Test timed out'
        elif outcome.failureDetail.notInstalled:
          details = 'App failed to install'
        # otherNativeCrash is not mutually exclusive to other failureDetails
        crash = _NATIVE_CRASH if outcome.failureDetail.otherNativeCrash else ''
        if details and crash:
          return '{d} ({c})'.format(d=details, c=crash)
        elif details:
          return details
        elif crash:
          return crash
      return _GetFailedCountDetails(step)

    elif outcome.summary == summary_enum.inconclusive:
      if outcome.inconclusiveDetail:
        if outcome.inconclusiveDetail.infrastructureFailure:
          return _INFRASTRUCTURE_FAILURE
        if outcome.inconclusiveDetail.abortedByUser:
          return 'Test run aborted by user'
      return 'Unknown reason'

    elif outcome.summary == summary_enum.skipped:
      if outcome.skippedDetail:
        if outcome.skippedDetail.incompatibleDevice:
          return 'Incompatible device/OS combination'
        if outcome.skippedDetail.incompatibleArchitecture:
          return 'App does not support the device architecture'
        if outcome.skippedDetail.incompatibleAppVersion:
          return 'App does not support the OS version'
      return 'Unknown reason'

    else:
      return 'Unknown outcome'


def _GetFailedCountDetails(step):
  """Build a string with status count sums for a step's testSuiteOverviews."""
  if not step.testExecutionStep:
    return 'Unknown failure'
  total = 0
  error = 0
  failed = 0
  skipped = 0
  for overview in step.testExecutionStep.testSuiteOverviews:
    total += overview.totalCount or 0
    error += overview.errorCount or 0
    failed += overview.failureCount or 0
    skipped += overview.skippedCount or 0

  if total:
    msg = '{f} test cases failed'.format(f=failed)
    passed = total - error - failed - skipped
    if passed:
      msg = '{m}, {p} passed'.format(m=msg, p=passed)
    if error:
      msg = '{m}, {e} errors'.format(m=msg, e=error)
    if skipped:
      msg = '{m}, {s} skipped'.format(m=msg, s=skipped)
    return msg
  else:
    return 'Test failed to run'
