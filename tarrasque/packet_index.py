from protobuf.impl import demo_pb2 as pb_d

def _bin_search(lst, f):
    """
    Searches a sorted list for an index where f(lst[i]) = 0 or f(lst[i-1]) !=
    f(lst[i]).
    """
    t = len(lst)
    b = 0
    while t > b:
        m = (t + b) // 2
        v = f(lst[m])
        if v == 0:
            return m
        elif v == -1:
            b = m
        elif v == 1:
            t = m
    return b

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

    def _search_packets_by_func(self, func):
        """
        Performs a binary search using the given comparison function and then
        returns the full packets and packets needed to recreate the game state
        at the point that the comparison function indicated.
        """
        p_index = _bin_search(self.packets, func)
        fpi = [i for i in self.full_indexes if i <= p_index]
        fps = [self.packets[i] for i in fpi]
        ps = self.packets[fpi[-1]:p_index+1]
        return fps, ps

    def packets_for_tick(self, tick):
        """
        Returns the packets needed to reconstruct the match state for the given tick.
        """
        def index_f(entity):
            peek, _ = entity
            if peek.tick < tick:
                return -1
            elif peek.tick == tick:
                return 0
            elif peek.tick > tick:
                return 1
            assert False

        return self._search_packets_by_func(index_f)

    def __iter__(self):
        return PacketIter(self)

    def __repr__(self):
        fmt = "<PacketIndex: {} fp, {} p>"
        return fmt.format(len(self.full_indexes), len(self.packets))