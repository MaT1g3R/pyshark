from pyshark.capture.capture import Capture
from pyshark.tshark.tshark import get_tshark_interfaces


class LiveCapture(Capture):
    """
    Represents a live capture on a network interface.
    """

    def __init__(self, interface=None, bpf_filter=None, display_filter=None, only_summaries=False):
        """
        Creates a new live capturer on a given interface. Does not start the actual capture itself.

        :param interface: Name of the interface to sniff on. If not given, takes the first available.
        :param bpf_filter: BPF filter to use on packets.
        :param display_filter: Display (wireshark) filter to use.
        :param only_summaries: Only produce packet summaries, much faster but includes very little information
        """
        super(LiveCapture, self).__init__(display_filter=display_filter, only_summaries=only_summaries)
        self.bpf_filter = bpf_filter
        
        if interface is None:
            self.interfaces = get_tshark_interfaces()
        else:
            self.interfaces = [interface]

    def get_parameters(self, packet_count=None):
        """
        Returns the special tshark parameters to be used according to the configuration of this class.
        """
        params = super(LiveCapture, self).get_parameters(packet_count=packet_count)
        for interface in self.interfaces:
            params += ['-i', interface]
        if self.bpf_filter:
            params += ['-f', self.bpf_filter]
        return params

    # Backwards compatibility
    sniff = Capture.load_packets

    def sniff_continuously(self, packet_count=None):
        """
        Captures from the set interface, returning a generator which returns packets continuously.

        Can be used as follows:
        for packet in capture.sniff_continuously();
            print 'Woo, another packet:', packet

        :param packet_count: an amount of packets to capture, then stop.
        """
        # Retained for backwards compatibility and to add documentation.
        return self.packets_from_tshark(packet_count=packet_count)