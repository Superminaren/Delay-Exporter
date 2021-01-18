# Delay-Exporter
 Prometheus exporter for Stockholm County Bus traffic

 Included is a service file for systemd.

 Requirements:
 - Python 3
 - Installing contents on 

 Install Instructions:
 - Run **install.sh** as root
 - Verify installation by running **systemctl status prometheus-sl-exporter**
 - Visiting http://<ADDRESS>:8000/ to verify, or running **curl http://localhost:8000/