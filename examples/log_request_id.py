import uuid
import logging
from sanic import Sanic
from sanic import response
from sanic import taskcontext
from multiprocessing import cpu_count

log = logging.getLogger(__name__)


class RequestIdFilter(logging.Filter):
    def filter(self, record):
        record.request_id = taskcontext.get('X-Request-ID')
        return True


LOG_SETTINGS = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'level': 'DEBUG',
            'formatter': 'default',
            'filters': ['requestid'],
        },
    },
    'filters': {
        'requestid': {
            '()': RequestIdFilter,
        },
    },
    'formatters': {
        'default': {
            'format': '%(asctime)s %(levelname)s %(name)s:%(lineno)d %(request_id)s | %(message)s',
        },
    },
    'loggers': {
        '': {
            'level': 'DEBUG',
            'handlers': ['console'],
            'propagate': True
        },
    }
}

app = Sanic(__name__, log_config=LOG_SETTINGS)


@app.middleware('request')
async def set_request_id(request):
    request_id = request.headers.get('X-Request-ID') or str(uuid.uuid4())
    taskcontext.set("X-Request-ID", request_id)


@app.route("/")
async def test(request):
    log.debug('X-Request-ID: %s', taskcontext.get('X-Request-ID'))
    log.info('Hello from test!')
    return response.json({"test": True})


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8000, workers=cpu_count())
