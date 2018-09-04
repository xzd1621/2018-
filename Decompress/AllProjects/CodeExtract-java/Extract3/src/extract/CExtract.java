package extract;

import bean.FunParams;
import org.apache.commons.lang.StringUtils;

import java.util.ArrayList;
import java.util.List;
import java.util.regex.Matcher;
import java.util.regex.Pattern;


/**
 * C language
 *
 * @author xu
 *
 */
public class CExtract {

    /**
    *返回类型　<> 或[]或*或& 函数名(参数列表)
     *  (\s+[\*&]*\s*)|(\s*[\*&]*\s+)　是为了匹配形如 int *f() 和int* f()这两种形式
     *  \((.*?\s*.*?)\s*\) 因为.*?不匹配换行，所以要多匹配几行。可以在最后一个.*?后面加上多个\s*.*?
    **/
    public static Pattern C_PATTERN = Pattern.compile("((\\w+<*\\w*>*\\[*]*\\w*)((\\s+[\\*&]*\\s*)|(\\s*[\\*&]*\\s+))(\\w+)\\s*\\((.*?\\s*.*?)\\s*\\))");
    /**
     * 提取函数参数
     *
     * @param code
     * @return
     */
    public static List<FunParams> extractfunction(String code) {
        List<FunParams> list = new ArrayList<FunParams>();

        //提取常规方法
        Matcher m =C_PATTERN.matcher(code);
        while (m.find()) {
            String fun=m.group(6);
            //排除关键字的干扰
            if ( !fun.equals("main") && !fun.contains("throw")
                    && !m.group(2).equals("new") && !m.group(2).equals("return") && !fun.equals("if")
                    &&!m.group(2).contains("throw")&&!fun.contains("this")&&!fun.equals("while")
                    &&!fun.equals("super")&&!fun.equals("for")&&!fun.equals("sizeof")
                    &&!fun.equals("void")&&!m.group(2).equals("typedef") &&!fun.equals("defined")
                    &&!fun.equals("free")) {
                FunParams funParams = new FunParams();
                if (!StringUtils.isEmpty(m.group(7).trim())){//参数列表不为空
                    boolean flag=true;//判断是否为函数形式的参数列表
                    String []params=m.group(7).trim().replace("\n", "").split(",");//参数列表以,分开
                    for(int i=0;i<params.length;i++)
                    {
                        if(params!=null&&params.length==1&&params[0].contains("void"))//排除形如int main(void)形式的
                            break;
                        if(params[i]==null||params[i].split(" ").length==1)
                        {
                            flag=false;//排除形似函数形式的 ，如参数列表为(A, int b)这种形式
                            break;
                        }
                    }
                    if(flag==true)//如果是函数形式的
                    {
                        funParams.setFunction(fun);
                        funParams.setParams(params);
                    }
                }
                else {//参数列表为空
                    funParams.setFunction(fun);
                    String empty[] = {};
                    funParams.setParams(empty);
                }
                if (!list.contains(funParams)&&funParams.getFunction()!=null) {
                    list.add(funParams);
                }
            }
        }
        return list;
    }
}
