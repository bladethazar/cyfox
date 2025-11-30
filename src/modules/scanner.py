"""Network vulnerability scanner module (Bjorn-inspired)"""
# pylint: disable=duplicate-code
import threading
import ipaddress
import time
from typing import List, Dict, Optional, Callable
from datetime import datetime
import socket
from src.core.config import Config
from src.core.state import StateManager, CyfoxState


class ScanResult:
    """Represents a network scan result"""

    def __init__(self, host: str, ports: List[int], services: Dict[str, str],
                 vulnerabilities: List[str] = None):
        self.host = host
        self.ports = ports
        self.services = services
        self.vulnerabilities = vulnerabilities or []
        self.timestamp = datetime.now()

    def to_dict(self) -> Dict:
        """Convert to dictionary"""
        return {
            'host': self.host,
            'ports': self.ports,
            'services': self.services,
            'vulnerabilities': self.vulnerabilities,
            'timestamp': self.timestamp.isoformat()
        }

    # pylint: disable=too-few-public-methods


class NetworkScanner:
    """Network vulnerability scanner (Bjorn-inspired)"""

    def __init__(self, config: Config, state_manager: StateManager):
        # pylint: disable=too-many-instance-attributes
        self.config = config
        self.state_manager = state_manager
        self.scan_interval = config.get('cyfox.scanner.scan_interval', 3600)
        self.network_range = config.get('cyfox.scanner.network_range', '192.168.1.0/24')
        self.ports = config.get('cyfox.scanner.ports', [22, 80, 443, 445, 3306, 3389])
        self.running = False
        self.thread: Optional[threading.Thread] = None
        self.scan_results: List[ScanResult] = []
        self.callback: Optional[Callable] = None
        self.last_scan: Optional[datetime] = None

    def register_callback(self, callback: Callable):
        """Register callback for scan completion"""
        self.callback = callback

    def _scan_host(self, host: str) -> Optional[ScanResult]:
        """Scan a single host"""
        try:
            # Use nmap if available, otherwise use simple port scan
            open_ports = []
            services = {}

            # Simple port scan using socket (fallback if nmap not available)
            for port in self.ports:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(0.5)
                result = sock.connect_ex((host, port))
                sock.close()

                if result == 0:
                    open_ports.append(port)
                    # Try to identify service
                    service_name = self._identify_service(port)
                    services[str(port)] = service_name

            if open_ports:
                # Check for vulnerabilities (simplified)
                vulnerabilities = self._check_vulnerabilities(host, open_ports, services)
                return ScanResult(host, open_ports, services, vulnerabilities)

        except Exception as e:  # pylint: disable=broad-exception-caught
            print(f"Error scanning {host}: {e}")

        return None

    def _identify_service(self, port: int) -> str:
        """Identify service by port"""
        common_ports = {
            22: 'SSH',
            80: 'HTTP',
            443: 'HTTPS',
            445: 'SMB',
            3306: 'MySQL',
            3389: 'RDP',
            21: 'FTP',
            23: 'Telnet',
        }
        return common_ports.get(port, f'Unknown-{port}')

    def _check_vulnerabilities(self, host: str, ports: List[int],
                              services: Dict[str, str]) -> List[str]:
        """Check for common vulnerabilities (simplified)"""
        # pylint: disable=unused-argument
        vulnerabilities = []

        # Check for common vulnerable services
        if 3306 in ports:
            vulnerabilities.append("MySQL port exposed - check for weak credentials")
        if 445 in ports:
            vulnerabilities.append("SMB port exposed - check for EternalBlue vulnerability")
        if 3389 in ports:
            vulnerabilities.append("RDP port exposed - check for BlueKeep vulnerability")
        if 21 in ports:
            vulnerabilities.append("FTP port exposed - check for anonymous access")

        return vulnerabilities

    def scan_network(self) -> List[ScanResult]:
        """Scan the configured network range"""
        results = []

        try:
            network = ipaddress.ip_network(self.network_range, strict=False)
            hosts = list(network.hosts())[:10]  # Limit to first 10 hosts for performance

            self.state_manager.state = CyfoxState.SCANNING

            for host in hosts:
                result = self._scan_host(str(host))
                if result:
                    results.append(result)

            self.scan_results = results
            self.last_scan = datetime.now()

            # Return to idle after scan
            if self.state_manager.mode.name != 'SCANNER':
                self.state_manager.state = CyfoxState.IDLE

            return results

        except Exception as e:  # pylint: disable=broad-exception-caught
            print(f"Error scanning network: {e}")
            self.state_manager.state = CyfoxState.IDLE
            return []

    def _periodic_scan(self):
        """Periodic scanning thread"""
        while self.running:
            if self.state_manager.mode.name == 'SCANNER':
                results = self.scan_network()
                if self.callback and results:
                    try:
                        self.callback(results)
                    except Exception as e:  # pylint: disable=broad-exception-caught
                        print(f"Error in scanner callback: {e}")

            # Wait for scan interval
            time.sleep(self.scan_interval)

    def start(self):
        """Start periodic scanning"""
        if self.running:
            return

        self.running = True
        self.thread = threading.Thread(target=self._periodic_scan, daemon=True)
        self.thread.start()

    def stop(self):
        """Stop scanning"""
        self.running = False
        if self.thread:
            self.thread.join(timeout=5.0)

    def get_results(self) -> List[ScanResult]:
        """Get latest scan results"""
        return self.scan_results