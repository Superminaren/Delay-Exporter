# Delay-Exporter

 Prometheus exporter for Stockholm County Bus traffic metrics.


# Metrics
    - traffic_delay_seconds
    - traffic_delay_count
    - traffic_count~~~~

# Installation

 Included:
 - Service file for systemd
 - Config file 

 Requirements:
 - Python 3
 - Root access (To install)


 Running without installing:
 - Run **Exporter.py path_to_config**

 Install Instructions (Simple)
 - Run **install_auto.sh** as root
 - Verify installation by running **systemctl status prometheus-sl-exporter**
 - Visiting http://ADDRESS:8000/ to verify, or running **curl http://localhost:8000/  

 Install instructions (More elaborate):
 - Run **install.sh** as root
 - Manually create a new user for the service in /etc/systemd/system/prometheus-sl-exporter.service, then change it.
 - Then run **systemctl daemon-reload && systemctl restart prometheus-sl-exporter** as root.
 - Verify installation by running **systemctl status prometheus-sl-exporter**
 - Visiting http://ADDRESS:8000/ to verify, or running **curl http://localhost:8000/**  

 TODO: 
  - Fully manual install instructions
  - Setting listen address in config
  - Catch further edge cases
  - 

 # Configuration

