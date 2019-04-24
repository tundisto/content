import demistomock as demisto
from CommonServerPython import *
from CommonServerUserPython import *
'''IMPORTS'''
import time
import random
from faker import Faker
from faker.providers import internet

try:
    '''SETUP'''
    fake = Faker()
    fake.add_provider(internet)

    indicators_count = 1000
    per_batch = 1000
    executions = int(indicators_count / per_batch)

    indicator_types = [fake.email, fake.ipv4, fake.url]

    indicators = []
    for i in range(indicators_count):
        idx = random.randint(0, len(indicator_types) - 1)
        indicator = indicator_types[idx]().replace('.', '[.]') if idx != 0 else indicator_types[idx]()
        if idx == 2:
            indicator = indicator.replace('http', 'hxxp')
        indicators.append(indicator)

    indicators_texts = []
    for i in range(1, executions + 1):
        text = '\n'.join(indicators[(i - 1) * per_batch: i * per_batch])
        indicators_texts.append(text)

    '''EXECUTION'''
    start_time = time.perf_counter()
    for indicators_text in indicators_texts:
        res = demisto.executeCommand('extractIndicators', {'text': indicators_text})
    end_time = time.perf_counter()
    delta = end_time - start_time
    performance_msg = 'Formatting scripts execution time for a total of '
    performance_msg += '{} indicators in batches of {} for a total of {}'.format(indicators_count, per_batch, executions)
    performance_msg += ' executions: {}'.format(delta)
    entry_context = {'Formatting.Time': delta}
    return_outputs(readable_output=performance_msg, outputs=entry_context, raw_response=res)
except Exception as e:
    return_error(str(e))
