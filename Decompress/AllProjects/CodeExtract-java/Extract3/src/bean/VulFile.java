package bean;

/**
 * description:
 *
 * @htyi
 * @create 2018-07-14 下午6:28
 * ＊＠棱镜七彩
 **/
public class VulFile {
    private String cve_id;
    private String cnnvd_id;

    public VulFile() {

    }

    public VulFile(String cve_id, String cnnvd_id) {
        this.cve_id = cve_id;
        this.cnnvd_id = cnnvd_id;
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
