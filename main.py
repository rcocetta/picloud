from picloudsync import PiCloudSync
from settings import CFG

sync = PiCloudSync(CFG)
sync.run()