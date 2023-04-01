from PyQt5 import QtCore, QtWidgets, uic
from PyQt5.QtCore import QTimer
import pyqtgraph as pg
import psutil
import sys

class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, *args, **kwargs):
        self.log1 = ([], [])
        self.log2 = ([], [])

        self.count = 0
        self.max_count = 20

        self.l_bt = None
        self.l_bs = None
        self.l_br = None
        self.l_ps = None
        self.l_pr = None
        self.l_pt = None

        super(MainWindow, self).__init__(*args, **kwargs)

        uic.loadUi('gui.ui', self)

        graph_style = {"font-size": "15px", "color": "white"}

        self.dataGraph.setTitle("kB/s", **graph_style)
        self.dataGraph.setLabel("left", "Data", **graph_style)
        self.dataGraph.setBackground("#646464")
        self.dataGraph.showGrid(x=True, y=True)

        self.pktGraph.setTitle("Pkt/s", **graph_style)
        self.pktGraph.setLabel("left", "Packets", **graph_style)
        self.pktGraph.setBackground("#646464")
        self.pktGraph.showGrid(x=True, y=True)

        self.qTimer = QTimer()
        self.qTimer.setInterval(1000)
        self.qTimer.timeout.connect(self.network_monitor)
        self.qTimer.start()

    def update_data_graph(self, count, data):
        self.dataGraph.plot(count, data, pen=pg.mkPen(color=(255, 0, 0)))
    
    def update_pkt_graph(self, count, data):
        self.pktGraph.plot(count, data, pen=pg.mkPen(color=(255, 0, 0)))
    
    def network_monitor(self):
        io = psutil.net_io_counters()
        bs, br, ps, pr = io.bytes_sent, io.bytes_recv, io.packets_sent, io.packets_recv
        bt = bs + br # 6 bytetotal
        pt = ps + pr # 7 pkttotal

        bps = bt - self.l_bt if self.l_bt else 0  # 0 bytetotal/sec
        bsps = bs - self.l_bs if self.l_bs else 0 # 1 bytesent/sec
        brps = br - self.l_br if self.l_br else 0 # 2 byterecv/sec
        psps = ps - self.l_ps if self.l_ps else 0 # 3 pktsent/sec
        prps = pr - self.l_pr if self.l_pr else 0 # 4 pktrecv/sec
        ptps = pt - self.l_pt if self.l_pt else 0 # 5 pkttotal/sec

        self.l_bt = bt
        self.l_bs = bs
        self.l_br = br
        self.l_ps = ps
        self.l_pr = pr
        self.l_pt = pt

        self.log1[0].append(self.count)
        self.log1[1].append(bps/1000)
        self.log1[0].pop(0) if len(self.log1[0]) > self.max_count else None
        self.log1[1].pop(0) if len(self.log1[1]) > self.max_count else None
        self.dataGraph.clear()

        self.log2[0].append(self.count)
        self.log2[1].append(ptps)
        self.log2[0].pop(0) if len(self.log2[0]) > self.max_count else None
        self.log2[1].pop(0) if len(self.log2[1]) > self.max_count else None
        self.pktGraph.clear()
        
        self.dataTotal.setText(self.byte_show(bt))
        self.pktTotal.setText(str(f"{pt / 1000}K" if pt > 1000 else pt))

        self.count += 1

        self.update_data_graph(self.log1[0], self.log1[1])
        self.update_pkt_graph(self.log2[0], self.log2[1])

    def byte_show(self, num, space=7):
        if num > 1e+9:
            return f"{(num / 1e+9):.2f}{' ' * (space - len(f'{(num / 1e+9):.2f}'))}GB"
        elif num > 1000000:
            return f"{(num / 1000000):.2f}{' ' * (space - len(f'{(num / 1000000):.2f}'))}MB"
        elif num > 1000:
            return f"{(num / 1000):.2f}{' ' * (space - len(f'{(num / 1000):.2f}'))}kB"
        else:
            return f"{(num):.2f}{' ' * (space - len(f'{(num):.2f}'))}B"

def main():
    app = QtWidgets.QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
