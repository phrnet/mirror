#
# Copyright (C) 2013 Shang Yuanchun <idealities@gmail.com>
#
#
# You may redistribute it and/or modify it under the terms of the
# GNU General Public License, as published by the Free Software
# Foundation; either version 3 of the License, or (at your option)
# any later version.
#
# mirror is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with mirror. If not, write to:
#   The Free Software Foundation, Inc.,
#   51 Franklin Street, Fifth Floor
#   Boston, MA  02110-1301, USA.
#
#

import os, sys
import time
import mmap
import struct
import cPickle as pickle
import mirror.color
import mirror.task  as task
import mirror.error as error

TASK_DESC = {
            task.REGULAR_TASK: "Normal task",
            task.TIMEOUT_TASK: "Timeout check",
            }

def list_task_queue():
    try:
        bufferfd = os.open("/tmp/mirrord", os.O_RDONLY)
    except:
        print >> sys.stderr, _("Open /tmp/mirrord failed, "
                               "can't read task infomation")
        return error.MIRROR_NOFILE

    buffer = mmap.mmap(bufferfd, os.fstat(bufferfd).st_size,
                       mmap.MAP_SHARED, mmap.PROT_READ)
    buffer.seek(2)
    size = struct.unpack("I", buffer.read(4))[0]

    taskqueue = pickle.loads(buffer.read(size))
    formatstr = ("Task:"+mirror.color.FOREGROUND_COLORS.GREEN
                +"%-18s"+mirror.color.COLOR_END+"\ttype:%14s\ttime: %s")
    for taskinfo in taskqueue:
        print formatstr % (
              taskinfo.name, TASK_DESC[taskinfo.tasktype],
              time.asctime(time.localtime(taskinfo.time)))

    buffer.close()
    os.close(bufferfd)
    return error.MIRROR_OK

def signal_process(signame):
    if signame not in ('stop', 'reload'):
        print >> sys.stderr, _("Invalid value for -s, "
                               "available: stop, reload")
        return error.MIRROR_ERRARG
    return error.MIRROR_OK
