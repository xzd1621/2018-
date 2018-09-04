package bean;

/**
 * description:
 *
 * @htyi
 * @create 2018-07-14 下午2:51
 * ＊＠棱镜七彩
 **/
public class Vul {
    private String cve_id;
    private String cnnvd_id;
    private String severity; //漏洞等级

    public Vul(){

    }

    public Vul(String cve_id,String cnnvd_id,String severity){
        this.cve_id = cve_id;
        this.cnnvd_id = cnnvd_id;
        this.severity = severity;
    }

    public String getSeverity() {
        return severity;
    }

    public void setSeverity(String severity) {
        this.severity = severity;
    }

    public String getCve_id() {
        return cve_id;
    }

    public void setCve_id(String cve_id) {
        this.cve_id = cve_id;
    }

    public String getCnnvd_id() {
        return cnnvd_id;
    }

    public void setCnnvd_id(String cnnvd_id) {
        this.cnnvd_id = cnnvd_id;
    }
}
