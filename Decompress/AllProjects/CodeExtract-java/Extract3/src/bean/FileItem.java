package bean;


/**
 * description:
 *
 * @htyi
 * @create 2018-07-14 下午2:37
 * ＊＠棱镜七彩
 **/
public class FileItem {
    private String key;  //md5
    private String path;

    public FileItem(){

    }

    public FileItem(String key,String path){
        this.key = key;
        this.path = path;
    }

    public String getKey() {
        return key;
    }

    public void setKey(String key) {
        this.key = key;
    }

    public String getPath() {
        return path;
    }

    public void setPath(String path) {
        this.path = path;
    }
}
