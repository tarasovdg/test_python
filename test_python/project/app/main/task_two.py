import json
import random
from queue import Queue
from os import path, walk
from operator import itemgetter
from threading import Thread

from flask import jsonify

from .view import main

file_path = 'project/app/test_file'
max_timeout = 2


@main.route('/task_two')
def page_task_two():
    """
    Api второго задания
    :return:
    """
    thr = list()
    queue = Queue()
    results = []
    for __, __, file_names in walk(file_path):
        if len(file_names):
            for i, one_file in enumerate(file_names):
              thr.append(Thread(target=read_file, args=(file_path, one_file, queue)))
              thr[i].start()
    for i in thr:
        i.join()
    for i in thr:
        results = results + queue.get()
    return jsonify(sorted(results, key=itemgetter('id')))


def read_file(file_path: str, one_file: str, queue: Queue):
    """
    Парс файлов
    :param file_path:
    :param one_file:
    :param queue:
    :return:
    """
    result = []
    with open(path.join(file_path, one_file)) as input_file:
        for line in input_file:
            try:
                # имитация задержки
                if random.randrange(4) > max_timeout:
                    raise Exception
                result.append(json.loads(line))
            except Exception:
                continue

    queue.put(result)
