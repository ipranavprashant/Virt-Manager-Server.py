import libvirt
import time

# Function to monitor CPU usage
def get_cpu_usage(domain):
    stats = domain.interfaceStats('eth0')  # Change interface name if needed
    return stats[0]  # Return CPU usage percentage (for example)

# Function to check if CPU usage exceeds threshold
def check_cpu_usage():
    conn = libvirt.open('qemu:///system')
    domain = conn.lookupByName('server-1')  # Replace with your VM name
    cpu_usage = get_cpu_usage(domain)
    print(f"Current CPU usage: {cpu_usage}%")
    
    if cpu_usage > 80:  # Example threshold
        print("CPU usage is too high! Spawning a new server.")
        spawn_new_vm()
    
    conn.close()

# Function to spawn a new VM
def spawn_new_vm():
    conn = libvirt.open('qemu:///system')
    xml = """<domain type='kvm'>
                <name>server-2</name>
                <memory unit='KiB'>1048576</memory>
                <vcpu placement='static'>1</vcpu>
                <os>
                    <type arch='x86_64' machine='pc-i440fx-2.9'>hvm</type>
                    <boot dev='hd'/>
                </os>
                <devices>
                    <disk type='file' device='disk'>
                        <driver name='qemu' type='qcow2'/>
                        <source file='/var/lib/libvirt/images/server-2.qcow2'/>
                        <target dev='vda' bus='virtio'/>
                    </disk>
                    <interface type='network'>
                        <mac address='52:54:00:ae:ad:01'/>
                        <source bridge='virbr0'/>
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
