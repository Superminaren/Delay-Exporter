# Delay-Exporter

#NOT FINISHED

 Prometheus exporter for Stockholm County Bus traffic

 Included is a service file for systemd.

 Requirements:
 - Python 3
 - Root access (To install)


 Running without installing:
 - Run Exporter.py 

 Install Instructions (Simple)
 - Run **install_auto.sh** as root
 - Verify installation by running **systemctl status prometheus-sl-exporter**
 - Visiting http://<ADDRESS>:8000/ to verify, or running **curl http://localhost:8000/  

 Install instructions (More elaborate):
 - Run **install_auto.sh** as root
 - Manually create a new user for the service in /etc/systemd/system/prometheus-sl-exporter.service, then change it.
 - Then run **systemctl daemon-reload && systemctl restart prometheus-sl-exporter** as root.
 - Verify installation by running **systemctl status prometheus-sl-exporter**
 - Visiting http://ADDRESS:8000/ to verify, or running **curl http://localhost:8000/**  

 TODO: Fully manual install instructions:
 