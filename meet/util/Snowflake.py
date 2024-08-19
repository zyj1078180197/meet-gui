import time
import random

# 定义雪花算法的基本参数
WORKER_ID_BITS = 5
DATACENTER_ID_BITS = 5
SEQUENCE_BITS = 12

# 最大的工作ID和数据中心ID
MAX_WORKER_ID = -1 ^ (-1 << WORKER_ID_BITS)  # 2**5 - 1
MAX_DATACENTER_ID = -1 ^ (-1 << DATACENTER_ID_BITS)

# 序列号掩码
SEQUENCE_MASK = -1 ^ (-1 << SEQUENCE_BITS)

# 工作ID和数据中心ID偏移量
WORKER_ID_SHIFT = SEQUENCE_BITS
DATACENTER_ID_SHIFT = SEQUENCE_BITS + WORKER_ID_BITS
TIMESTAMP_LEFT_SHIFT = SEQUENCE_BITS + WORKER_ID_BITS + DATACENTER_ID_BITS

# 时间基准点
TWEPOCH = 1288834974657


class Snowflake:
    def __init__(self, datacenterId, workerId, sequence=0):
        if datacenterId > MAX_DATACENTER_ID or datacenterId < 0:
            raise ValueError(f'Datacenter ID {datacenterId} is invalid')
        if workerId > MAX_WORKER_ID or workerId < 0:
            raise ValueError(f'Worker ID {workerId} is invalid')
        if sequence > SEQUENCE_MASK:
            raise ValueError(f'Sequence {sequence} is invalid')

        self.datacenterId = datacenterId
        self.workerId = workerId
        self.sequence = sequence
        self.lastTimestamp = -1

    @staticmethod
    def _tilNextMillis(lastTimestamp):
        timestamp = int(time.time() * 1000)
        while timestamp <= lastTimestamp:
            timestamp = int(time.time() * 1000)
        return timestamp

    def generate(self):
        timestamp = int(time.time() * 1000)

        if self.lastTimestamp == timestamp:
            self.sequence = (self.sequence + 1) & SEQUENCE_MASK
            if self.sequence == 0:
                timestamp = self._tilNextMillis(self.lastTimestamp)
        else:
            self.sequence = 0

        if timestamp < self.lastTimestamp:
            raise ValueError('Clock moved backwards. Refusing to generate id for %d milliseconds' % (
                    self.lastTimestamp - timestamp))

        self.lastTimestamp = timestamp

        return ((timestamp - TWEPOCH) << TIMESTAMP_LEFT_SHIFT) | \
            (self.datacenterId << DATACENTER_ID_SHIFT) | \
            (self.workerId << WORKER_ID_SHIFT) | \
            self.sequence


# 生成随机的工作机ID和数据中心ID
datacenterId = random.randint(0, MAX_DATACENTER_ID)
workerId = random.randint(0, MAX_WORKER_ID)

# 创建雪花算法实例
snowflake = Snowflake(datacenterId, workerId)

if __name__ == '__main__':
    for i in range(10):
        print(snowflake.generate())
