# Ambari-Elastic-Service

## Project
### Elasticsearch 6.4.x
|  Feature   |  Description       |
| -----------| -----------------|
| Version | 6.4.2 |
| Service | Elasticsearch |
| Component-Master | Elasticsearch-Master (node.master=true, node.data=true) |
| Component-Slave | Elasticsearch-Slave (node.master=flase, node.data=true)  |
| Extra | Including all X-Pack features |

### Kibana 6.4.x
In development...


## Prerequisite
|  Softwate   |  Version | Status  |
| -----------| -----------------| -----------------|
| Ambari | 2.x (test on 2.6.2.0) | Fully Installed |


## How to use
1. Download the source code.
2. Copy the project folder to ambari 's lib folder. Such as:
```
cp -r ./ELASTICSEARCH-6.4.x /var/lib/ambari-server/resources/stacks/HDP/2.6/services
```
3. Restart ambari-server:
```
ambari-server restart
```
4. Log into web then add service as usual. Such as:
![image](https://github.com/BalaBalaYi/Ambari-Elastic-Service/blob/master/doc/es-ambari-1.png)

5. Enjoy urself^^
