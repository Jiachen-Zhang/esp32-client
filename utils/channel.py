from queue import Queue, Full

RAW_CSI_QUEUE: Queue = Queue(maxsize=64)
MEAN_AMPLITUDE_CSI_QUEUE: Queue = Queue(maxsize=64)
