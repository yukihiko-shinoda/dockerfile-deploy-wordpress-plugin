class EventAnalyzer:
    def __init__(self, events):
        self.events = events

    @staticmethod
    def get_response(events):
        for event in events:
            if event['event'] == 'runner_on_ok' and event['event_data']['task_action'] == 'debug':
                return event['event_data']['res']

    @staticmethod
    def extract_result_debug(response, list_debug_variable):
        list_searching_debug_variable = list_debug_variable.copy()
        result_debug = {}
        for result in response['results']:
            if not list_searching_debug_variable:
                break
            EventAnalyzer.search_debug_value(result, list_searching_debug_variable, result_debug)
        return result_debug

    @staticmethod
    def search_debug_value(result, list_searching_debug_variable, result_debug):
        for searching_debug_variable in list_searching_debug_variable:
            if searching_debug_variable in result:
                result_debug[searching_debug_variable] = result[searching_debug_variable]
                list_searching_debug_variable.remove(searching_debug_variable)
                return
