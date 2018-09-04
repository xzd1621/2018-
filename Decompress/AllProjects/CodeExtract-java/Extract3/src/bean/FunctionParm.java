package bean;

import java.util.List;

/**
 * description:
 *
 * @htyi
 * @create 2018-07-14 下午2:43
 * ＊＠棱镜七彩
 **/
public class FunctionParm {
    private String function;
    private List<String> params;

    public String getFunction() {
        return function;
    }

    public void setFunction(String function) {
        this.function = function;
    }

    public List<String> getParams() {
        return params;
    }

    public void setParams(List<String> params) {
        this.params = params;
    }
}
