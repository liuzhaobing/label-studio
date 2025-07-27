import uuid
import traceback
from datetime import datetime

from pythonjsonlogger import jsonlogger

from label_studio.core.current_request import get_current_request


class CustomJsonFormatter(jsonlogger.JsonFormatter):
    def add_fields(self, log_record, record, message_dict):
        super(CustomJsonFormatter, self).add_fields(log_record, record, message_dict)
        request_id = None
        request = get_current_request()
        if request and 'X-Request-ID' in request.headers:
            request_id = request.headers['X-Request-ID']
        log_record['request_id'] = request_id

        # Add trace info
        log_record['traceId'] = getattr(record, 'traceId', '')
        log_record['spanId'] = '0.1'
        log_record['parentSpanName'] = 'label-studio'
        
        # Add environment info
        log_record['env'] = 'prod'  # Configure based on environment
        log_record['index'] = 'label_studio_logs'
        
        # Add request info
        log_record['ip'] = request.META.get('REMOTE_ADDR') if request else ''
        log_record['uri'] = request.path if request else ''
        
        # Add time in desired format
        log_record['time'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
        
        # Add execution context
        log_record['thread'] = record.threadName
        log_record['class'] = f"{record.name}.{record.funcName}:{record.lineno}"
        log_record['level'] = record.levelname
        
        # Add optional fields
        log_record['code'] = ''
        log_record['carrier'] = ''
        log_record['deviceId'] = ''
        log_record['platform'] = ''
        log_record['uid'] = record.user_id if hasattr(record, 'user_id') else ''
        log_record['stack_trace'] = ''
        if record.exc_info:
            log_record['stack_trace'] = ''.join(traceback.format_exception(*record.exc_info))
