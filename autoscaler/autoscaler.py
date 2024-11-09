import libvirt
import time

# Function to monitor CPU usage
def get_cpu_usage(domain):
    # Get the initial CPU time
    initial_stats = domain.getCPUStats(True)[0]
    initial_cpu_time = initial_stats['cpu_time']

    # Wait for a short interval to calculate the change
    time.sleep(1)

    # Get the CPU time again after 1 second
    final_stats = domain.getCPUStats(True)[0]
    final_cpu_time = final_stats['cpu_time']

    # Calculate CPU usage as a percentage
    cpu_time_diff = final_cpu_time - initial_cpu_time
    cpu_usage_percent = (cpu_time_diff / 1e9) * 100  # Convert nanoseconds to seconds and calculate percentage
    
    return cpu_usage_percent

# Function to check if CPU usage exceeds threshold
def check_cpu_usage():
    conn = libvirt.open('qemu:///system')
    domain = conn.lookupByName('ubuntu24.10')  # Replace with your VM name
    cpu_usage = get_cpu_usage(domain)
    print(f"Current CPU usage: {cpu_usage:.2f}%")
    
    if cpu_usage > 1:
        print("CPU usage is too high! Spawning a new server.")
        spawn_new_vm()
    
    conn.close()

# Function to spawn a new VM
def spawn_new_vm():
    conn = libvirt.open('qemu:///system')
    xml = """<domain type='kvm'>
                <name>prani</name>
                <memory unit='KiB'>1048576</memory>
                <vcpu placement='static'>1</vcpu>
                <os>
                    <type arch='x86_64' machine='pc-i440fx-2.9'>hvm</type>
                    <boot dev='hd'/>
                </os>
                <devices>
                    <disk type='file' device='disk'>
                        <driver name='qemu' type='qcow2'/>
                        <source file='/var/lib/libvirt/images/ubuntu24.10-2.qcow2'/>
                        <target dev='vda' bus='virtio'/>
                    </disk>
                    <interface type='network'>
                        <mac address='52:54:00:ae:ad:01'/>
                        <source network='default'/>  <!-- Replace 'default' with your actual network name -->
                        <model type='virtio'/>
                    </interface>
                </devices>
            </domain>"""

    
    domain = conn.createXML(xml, 0)  # Create the VM from the XML definition
    print(f"Created VM {domain.name()}")
    conn.close()

if __name__ == "__main__":
    while True:
        check_cpu_usage()  # Monitor CPU usage every 5 seconds
        time.sleep(5)
