#!/usr/bin/env python
"""
make_confidence_report.py
Usage:
  python make_confidence_report.py model.joblib

  where model.joblib is a file created by cleverhans.serial.save containing
  a picklable cleverhans.model.Model instance.

This script will run the model on a variety of types of data and save a
report to model_report.joblib. The report can be later loaded by another
script using cleverhans.serial.load. The format of the report is a dictionary.
Each dictionary key is the name of a type of data:
  clean : Clean data
  semantic : Semantic adversarial examples
  mc: MaxConfidence adversarial examples
Each value in the dictionary contains an array of bools indicating whether
the model got each example correct and an array containing the confidence
that the model assigned to each prediction.

This script works by running a single MaxConfidence attack on each example.
( https://openreview.net/forum?id=H1g0piA9tQ )
This provides a reasonable estimate of the true failure rate quickly, so
long as the model does not suffer from gradient masking.
However, this estimate is mostly intended for development work and not
for publication. A more accurate estimate may be obtained by running
make_confidence_report_bundled.py instead.
"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import tensorflow as tf
from tensorflow.python.platform import flags

from cleverhans.utils_tf import silence
from cleverhans.confidence_report import make_confidence_report
from cleverhans.confidence_report import BATCH_SIZE
from cleverhans.confidence_report import MC_BATCH_SIZE
from cleverhans.confidence_report import TRAIN_START
from cleverhans.confidence_report import TRAIN_END
from cleverhans.confidence_report import TEST_START
from cleverhans.confidence_report import TEST_END
from cleverhans.confidence_report import WHICH_SET
from cleverhans.confidence_report import NB_ITER
from cleverhans.confidence_report import BASE_EPS_ITER
from cleverhans.confidence_report import REPORT_PATH

silence()

FLAGS = flags.FLAGS

def main(argv=None):
  """
  Make a confidence report and save it to disk.
  """
  try:
    _name_of_script, filepath = argv
  except ValueError:
    raise ValueError(argv)
  make_confidence_report(filepath=filepath, test_start=FLAGS.test_start,
                         test_end=FLAGS.test_end, which_set=FLAGS.which_set,
                         report_path=FLAGS.report_path,
                         mc_batch_size=FLAGS.mc_batch_size,
                         batch_size=FLAGS.batch_size)

if __name__ == '__main__':
  flags.DEFINE_integer('train_start', TRAIN_START, 'Starting point (inclusive)'
                       'of range of train examples to use')
  flags.DEFINE_integer('train_end', TRAIN_END, 'Ending point (non-inclusive) '
                       'of range of train examples to use')
  flags.DEFINE_integer('test_start', TEST_START, 'Starting point (inclusive) of range'
                       ' of test examples to use')
  flags.DEFINE_integer('test_end', TEST_END, 'End point (non-inclusive) of range'
                       ' of test examples to use')
  flags.DEFINE_integer('nb_iter', NB_ITER, 'Number of iterations of PGD')
  flags.DEFINE_string('which_set', WHICH_SET, '"train" or "test"')
  flags.DEFINE_string('report_path', REPORT_PATH, 'Path to save to')
  flags.DEFINE_integer('mc_batch_size', MC_BATCH_SIZE,
                       'Batch size for MaxConfidence')
  flags.DEFINE_integer('batch_size', BATCH_SIZE,
                       'Batch size for most jobs')
  flags.DEFINE_float('base_eps_iter', BASE_EPS_ITER,
                     'epsilon per iteration, if data were in [0, 1]')
  tf.app.run()
