#Useful links
# https://www.shoreline.io/runbooks/tomcat/tomcat-jvm-outofmemory#


import subprocess

def run_command(command):
    try:
        result = subprocess.run(command, shell=True, check=True, text=True, capture_output=True)
        return result.stdout
    except subprocess.CalledProcessError as e:
        return f"Error running command '{command}': {e.stderr}"

def check_service_status(service_name):
    status_command = f"sudo systemctl status {service_name}"
    return run_command(status_command)

def main():
    tomcat_commands = {
	"Tomcat stuck threads, deadlocks, or high CPU usage": "sudo -u tomcat jstack -l <tomcat_pid>",
	"Monitor heap usage, garbage collection patterns": "sudo -u tomcat jstat -gcutil <tomcat_pid>"
    }
    nginx_commands = { "" }
    mysql_commands = { "" }
    commands = {
        "IP Address and Network Interfaces": "ip addr show",
        "Network Interfaces Status": "ip link show",
        "Routing Table": "ip route show",
        "Firewall Rules (iptables)": "sudo iptables -L -v -n",
        "Firewall Rules (firewalld)": "sudo firewall-cmd --list-all",
        "DNS Configuration": "cat /etc/resolv.conf",
        "DNS Resolution (google.com)": "nslookup google.com",
        "DNS Resolution (dig)": "dig google.com",
        "Test HTTP Connectivity (example.com)": "curl -v http://example.com",
        "SELinux Status": "sestatus",
        "AppArmor Status": "sudo aa-status",
        "Proxy Settings (HTTP)": "echo $http_proxy",
        "Proxy Settings (HTTPS)": "echo $https_proxy",
        "Default Gateway": "ip route show default",
        "Network Connectivity (ping example.com)": "ping -c 4 example.com",
        "Network Connectivity (mtr example.com)": "mtr -r -c 5 example.com",
        "CPU Usage": "top -b -n 1 | head -n 20",
        "I/O Statistics": "iostat",
        "System Load": "uptime",
        "Memory Usage": "free -h",
        "Swap Usage": "swapon -s",
        "Errors in /var/log/messages": "sudo tail -n 50 /var/log/messages",
        "Open File Handlers": "lsof | wc -l",
        "Open File Descriptors (Detailed)": "cat /proc/sys/fs/file-nr",
        "Inode Usage": "df -i",
        "Disk Usage": "df -h",
        "Network Bytes In/Out": "ifstat 1 1",
        "Problematic Processes (High CPU Usage)": "ps aux --sort=-%cpu | head -n 10",
        "Problematic Processes (High Memory Usage)": "ps aux --sort=-%mem | head -n 10",
        "Open Connections": "ss -tuln",
        "Kernel Related Errors": "sudo dmesg | tail -n 50",
        "Virtual Memory Statistics (vmstat)": "vmstat 1 5",
        "TCPDump (Readable Format)": "sudo tcpdump -n -i any -c 10 -A",
        "Process Listing (Detailed)": "ps auxf",
        "Network Statistics (netstat)": "netstat -s",
        "System Information (uname)": "uname -a",
        "System Logs (journalctl)": "sudo journalctl -n 50",
        "Mounted Filesystems": "mount",
        "Installed Packages (dpkg -l)": "dpkg -l",
        "System Uptime": "uptime",
        "System Environment Variables": "printenv",
        "Logged-in Users (who)": "who",
        "System File Permissions (sample directory)": "ls -l /home/pavan.tvba/",  # Replace /path/to/directory with actual path
        "Network Interface Configuration (ifconfig)": "ifconfig -a",
        "Disk I/O Wait Times (iostat)": "iostat -d 1 5",
	"Hardware specifications": "dmidecode",
        "Tomcat Status": check_service_status("tomcat"),
        "Nginx Status": check_service_status("nginx"),
        "MySQL Status": check_service_status("mysql"),
        "Node.js Status": check_service_status("node"),
    }

    results = {}

    for description, command in commands.items():
        if isinstance(command, str):
            results[description] = run_command(command)
        else:
            results[description] = command

    with open("troubleshoot_results.txt", "w") as f:
        for description, output in results.items():
            f.write(f"### {description} ###\n")
            f.write(output + "\n\n")

    print("Troubleshooting complete. Results saved in 'troubleshoot_results.txt'.")

if __name__ == "__main__":
    main()

