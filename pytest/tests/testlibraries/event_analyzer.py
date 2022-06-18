from typing import Any, cast, Dict, List


class EventAnalyzer:
    @staticmethod
    def get_response(events: List[Dict[str, Any]]) -> Dict[str, List[Dict[str, str]]]:
        for event in events:
            if event["event"] == "runner_on_ok" and event["event_data"]["task_action"] == "debug":
                return cast(Dict[str, List[Dict[str, str]]], event["event_data"]["res"])
        raise ValueError

    @staticmethod
    def extract_result_debug(
        response: Dict[str, List[Dict[str, Any]]], list_debug_variable: List[str]
    ) -> Dict[str, Any]:
        list_searching_debug_variable = list_debug_variable.copy()
        result_debug: Dict[str, Any] = {}
        for result in response["results"]:
            if not list_searching_debug_variable:
                break
            EventAnalyzer.search_debug_value(result, list_searching_debug_variable, result_debug)
        return result_debug

    @staticmethod
    def search_debug_value(
        result: Dict[str, Any], list_searching_debug_variable: List[str], result_debug: Dict[str, Any]
    ) -> None:
        for searching_debug_variable in list_searching_debug_variable:
            if searching_debug_variable in result:
                result_debug[searching_debug_variable] = result[searching_debug_variable]
                list_searching_debug_variable.remove(searching_debug_variable)
                return
