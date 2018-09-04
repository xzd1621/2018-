package bean;

import java.io.Serializable;
import java.util.ArrayList;
import java.util.List;

/**
 * description:
 *
 * @htyi
 * @create 2018-07-14 下午1:57
 * ＊＠棱镜七彩
 **/
public class EsProject implements Serializable{
    private String id;
    private String project_url;
    private String project_user;
    private String created_time;  //2018-01-01
    private String main_language;  //java
    private String project_name;
    private int project_id;
    private String latest_version = "";
    private List<String> official_license = new ArrayList<String>();
    private int project_fork;
    private int project_watch;
    private int project_star;
    private String full_name;
    private boolean is_library = false;   //默认为true 1   fasle　为　０,默认为不是组件
    private String version;
    private String homepage;
    private int popularity_level;   //分级　１　２　３　４　....
    private boolean is_vul_able = false; //是否有漏洞，默认没有
    private int total_vul_num = 0;
    private int high_vul_num = 0;
    private int mid_vul_num = 0;
    private int low_vul_num = 0;
    private List<VulFile> vul_list = new ArrayList<VulFile>();
    private List<VulFile> hig_vul_list = new ArrayList<VulFile>();
    private List<VulFile> mid_vul_list = new ArrayList<VulFile>();
    private List<VulFile> low_vul_list = new ArrayList<VulFile>();
    private String project_desc = "";
    private List<FileItem> items;
    private String soft_type = "";
    private List<String> dependencies = new ArrayList<String>();
    private String country = "";
    private List<String> os_platform = new ArrayList<String>();


    public String getVersion() {
        return version;
    }

    public void setVersion(String version) {
        this.version = version;
    }

    public String getId() {
        return id;
    }

    public void setId(String id) {
        this.id = id;
    }

    public String getProject_url() {
        return project_url;
    }

    public void setProject_url(String project_url) {
        this.project_url = project_url;
    }

    public String getProject_user() {
        return project_user;
    }

    public void setProject_user(String project_user) {
        this.project_user = project_user;
    }

    public String getCreated_time() {
        return created_time;
    }

    public void setCreated_time(String created_time) {
        this.created_time = created_time;
    }

    public String getMain_language() {
        return main_language;
    }

    public void setMain_language(String main_language) {
        this.main_language = main_language;
    }

    public String getProject_name() {
        return project_name;
    }

    public void setProject_name(String project_name) {
        this.project_name = project_name;
    }

    public int getProject_id() {
        return project_id;
    }

    public void setProject_id(int project_id) {
        this.project_id = project_id;
    }

    public String getLatest_version() {
        return latest_version;
    }

    public void setLatest_version(String latest_version) {
        this.latest_version = latest_version;
    }

    public List<String> getOfficial_license() {
        return official_license;
    }

    public void setOfficial_license(List<String> official_license) {
        this.official_license = official_license;
    }

    public int getProject_fork() {
        return project_fork;
    }

    public void setProject_fork(int project_fork) {
        this.project_fork = project_fork;
    }

    public int getProject_watch() {
        return project_watch;
    }

    public void setProject_watch(int project_watch) {
        this.project_watch = project_watch;
    }

    public int getProject_star() {
        return project_star;
    }

    public void setProject_star(int project_star) {
        this.project_star = project_star;
    }

    public String getFull_name() {
        return full_name;
    }

    public void setFull_name(String full_name) {
        this.full_name = full_name;
    }

    public boolean isIs_library() {
        return is_library;
    }

    public void setIs_library(boolean is_library) {
        this.is_library = is_library;
    }

    public String getProject_desc() {
        return project_desc;
    }

    public void setProject_desc(String project_desc) {
        this.project_desc = project_desc;
    }

    public String getHomepage() {
        return homepage;
    }

    public void setHomepage(String homepage) {
        this.homepage = homepage;
    }

    public int getPopularity_level() {
        return popularity_level;
    }

    public void setPopularity_level(int popularity_level) {
        this.popularity_level = popularity_level;
    }

    public boolean isIs_vul_able() {
        return is_vul_able;
    }

    public void setIs_vul_able(boolean is_vul_able) {
        this.is_vul_able = is_vul_able;
    }

    public int getTotal_vul_num() {
        return total_vul_num;
    }

    public void setTotal_vul_num(int total_vul_num) {
        this.total_vul_num = total_vul_num;
    }

    public int getHigh_vul_num() {
        return high_vul_num;
    }

    public void setHigh_vul_num(int high_vul_num) {
        this.high_vul_num = high_vul_num;
    }

    public int getMid_vul_num() {
        return mid_vul_num;
    }

    public void setMid_vul_num(int mid_vul_num) {
        this.mid_vul_num = mid_vul_num;
    }

    public int getLow_vul_num() {
        return low_vul_num;
    }

    public void setLow_vul_num(int low_vul_num) {
        this.low_vul_num = low_vul_num;
    }

    public List<FileItem> getItems() {
        return items;
    }

    public void setItems(List<FileItem> items) {
        this.items = items;
    }

    public String getSoft_type() {
        return soft_type;
    }

    public void setSoft_type(String soft_type) {
        this.soft_type = soft_type;
    }

    public List<String> getDependencies() {
        return dependencies;
    }

    public void setDependencies(List<String> dependencies) {
        this.dependencies = dependencies;
    }

    public String getCountry() {
        return country;
    }

    public void setCountry(String country) {
        this.country = country;
    }

    public List<String> getOs_platform() {
        return os_platform;
    }

    public void setOs_platform(List<String> os_platform) {
        this.os_platform = os_platform;
    }

    public List<VulFile> getVul_list() {
        return vul_list;
    }

    public void setVul_list(List<VulFile> vul_list) {
        this.vul_list = vul_list;
    }

    public List<VulFile> getHig_vul_list() {
        return hig_vul_list;
    }

    public void setHig_vul_list(List<VulFile> hig_vul_list) {
        this.hig_vul_list = hig_vul_list;
    }

    public List<VulFile> getMid_vul_list() {
        return mid_vul_list;
    }

    public void setMid_vul_list(List<VulFile> mid_vul_list) {
        this.mid_vul_list = mid_vul_list;
    }

    public List<VulFile> getLow_vul_list() {
        return low_vul_list;
    }

    public void setLow_vul_list(List<VulFile> low_vul_list) {
        this.low_vul_list = low_vul_list;
    }
}
