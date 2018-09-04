package bean;

public class FunParams {
    private String function;
    private String[] params;

    public String getFunction() {
        return function;
    }

    public void setFunction(String function) {
        this.function = function;
    }

    public String[] getParams() {
        return params;
    }

    //去除参数列表的首尾空格
    public void setParams(String[] params)
    {
        for (int i=0;i<params.length;i++)
        {
            params[i]=params[i].trim();
        }
        this.params=params;
    }
}
