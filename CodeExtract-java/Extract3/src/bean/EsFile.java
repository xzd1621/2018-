package bean;

import java.util.List;

/**
 * description:
 *
 * @htyi
 * @create 2018-07-14 下午2:42
 * ＊＠棱镜七彩
 **/
public class EsFile {
    private String id;   //md5
    private String content;
    private List<FunParams> function_param;
    private String path;   //"/java/md5.java"
    private String lang;  //"java"

    public String getId() {
        return id;
    }

    public void setId(String id) {
        this.id = id;
    }

    public String getContent() {
        return content;
    }

    public void setContent(String content) {
        this.content = content;
    }

    public String getPath() {
        return path;
    }

    public void setPath(String path) {
        this.path = path;
    }

    public String getLang() {
        return lang;
    }

    public void setLang(String lang) {
        this.lang = lang;
    }

    public List<FunParams> getFunction_param() {
        return function_param;
    }

    public void setFunction_param(List<FunParams> function_param) {
        this.function_param = function_param;
    }
}
