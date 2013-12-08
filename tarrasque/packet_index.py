from protobuf.impl import demo_pb2 as pb_d


class PacketIter(object):
    def __init__(self, pi):
        self.pi = pi
        self.pos = -1

    def __iter__(self):
        return self

    @property
    def current(self):
        return self.pi.packets[self.pos]

    def move(self, pos):
        self.pos = pos

    def next(self):
        self.pos += 1
        try:
            return self.pi.packets[self.pos]
        except IndexError:
            raise StopIteration()

    def prev(self):
        self.pos -= 1
        try:
            return self.pi.packets[self.pos]
        except IndexError:
            raise StopIteration()

    def reverse(self):
        while True:
            yield self.prev()

    def next_full(self):
        for packet in self:
            peek, _ = packet
            if peek.kind == pb_d.DEM_FullPacket:
                return packet
        raise StopIteration()

    def prev_full(self):
        for packet in self.reverse():
            peek, _ = packet
            if peek.kind == pb_d.DEM_FullPacket:
                return packet
        raise StopIteration()

    def next_packet(self):
        for packet in self:
            peek, _ = packet
            if peek.kind == pb_d.DEM_FullPacket:
                continue
            yield packet
        raise StopIteration()

    def prev_packet(self):
        for packet in self.reverse():
            peek, _ = packet
            if peek.kind == pb_d.DEM_FullPacket:
                continue
            yield packet
        raise StopIteration()

class PacketIndex(object):
    """
    A class to cache and manage queries onto the lists of full packets and
    packets.

    Internal representation of the full packets is more complex, with each
    packet being represented as a list, of the full packet, the index of the
    first packet for that full packet, and the number of packets for that full
    packet.
    """
    def __init__(self, packets, full_indexes):
        self.packets = packets
        self.full_indexes = full_indexes

    @classmethod
    def from_demoio(cls, demo):
        packets = []
        full_indexes = []
        for entry in demo:
            peek, _ = entry
            if peek.kind == pb_d.DEM_FullPacket:
                full_indexes.append(len(packets))
                packets.append(entry)
            elif peek.kind == pb_d.DEM_Packet:
                packets.append(entry)
        return cls(packets, full_indexes)

    def packets_for_tick(self, tick):
        """
        Returns the packets needed to reconstruct the match state for the given tick.
        """
        fpi = [i for i in self.full_indexes if self.packets[i][0].tick <= tick]
        fps = [self.packets[i] for i in fpi]
        ps = []
        for packet in self.packets[fpi[-1]+1:]:
            if packet[0].tick > tick:
                break
            ps.append(packet)

        return fps, ps

    def __iter__(self):
        return PacketIter(self)

    def __repr__(self):
        fmt = "<PacketIndex: {} fp, {} p>"
        return fmt.format(len(self.full_indexes), len(self.packets))
