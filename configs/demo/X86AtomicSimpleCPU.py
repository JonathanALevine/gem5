import m5
from m5.objects import *
from m5.objects import DDR4_2400_8x8
from m5.objects import DDR5_6400_4x8
import time


if __name__ == "__m5_main__":
    str_time = time.time()

    system = System()

    system.clk_domain = SrcClockDomain()
    system.clk_domain.clock = "5GHz"
    system.clk_domain.voltage_domain = VoltageDomain()

    system.mem_mode = "atomic"
    system.mem_ranges = [AddrRange("8192MB")]

    system.cpu = X86AtomicSimpleCPU()

    system.membus = SystemXBar()

    system.cpu.icache_port = system.membus.cpu_side_ports
    system.cpu.dcache_port = system.membus.cpu_side_ports

    system.cpu.createInterruptController()
    system.cpu.interrupts[0].pio = system.membus.mem_side_ports
    system.cpu.interrupts[0].int_requestor = system.membus.cpu_side_ports
    system.cpu.interrupts[0].int_responder = system.membus.mem_side_ports

    system.system_port = system.membus.cpu_side_ports

    system.mem_ctrl = MemCtrl()
    system.mem_ctrl.dram = DDR5_6400_4x8()
    system.mem_ctrl.dram.range = system.mem_ranges[0]
    system.mem_ctrl.port = system.membus.mem_side_ports

    # Workload to run on the cpu
    binary = "workloads/main"

    # for gem5 V21 and beyond
    system.workload = SEWorkload.init_compatible(binary)

    process = Process()
    process.cmd = [binary]
    system.cpu.workload = process
    system.cpu.createThreads()

    root = Root(full_system=False, system=system)
    m5.instantiate()

    print("Beginning simulation!")
    exit_event = m5.simulate()
    print(
        "Exiting @ tick {} because {}".format(
            m5.curTick(), exit_event.getCause()
        )
    )
    end_time = time.time()
    print(f"Execution time: {end_time-str_time} seconds")
    print(f"Execution time: {(end_time-str_time)/60} mins")
