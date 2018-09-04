/* extract the c++
* */
package extract;

import bean.FunParams;
import org.apache.commons.lang.StringUtils;

import java.util.ArrayList;
import java.util.List;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

public class CppExtract {

    /**
     * 匹配类名是为了提取构造函数
     * c++类的形式为class 类名 : 被继承的类
     * java 中类的形式为：class 类名 extends 被继承的类，　class 类名　implements 被实现的接口
     * 提取函数的正则表达式与Ｃ语言类似
     */

    public static Pattern CPP_CLASS_PATTERN = Pattern.compile("class\\s+(\\w+).*\\s*(:|\\{|extends|implements)");

    public static Pattern CPP_PATTERN = Pattern.compile("((\\w+<*\\w*>*\\[*]*\\w*)((\\s+[\\*&]*\\s*)|(\\s*[\\*&]*\\s+))(\\w+)\\s*\\((.*?\\s*.*?)\\s*\\))");

    /**
     * 提取类名(java   cpp需要)
     *
     * @param code
     */
    public static List<String> extractclass(String code) {
        ArrayList<String> classlist = new ArrayList<String>();
        Matcher m = CPP_CLASS_PATTERN.matcher(code);
        while (m.find()) {
            classlist.add(m.group(1).trim().replace("\n", ""));//去除首尾空格和换行
        }
        return classlist;
    }


    /**
     * 提取函数参数
     *
     * @param code
     * @return
     */
    public static List<FunParams> extractfunction(String code) {
        List<String> classlist = extractclass(code);
        List<FunParams> list = new ArrayList<FunParams>();
        //提取构造方法
        for (String i : classlist) {
            Pattern pattern = Pattern.compile("(.*?)\\s+" + i + "\\s*\\((.*?\\s*.*?)\\)\\s*"); //构造方法形式：修饰符　类名　参数列表
            Matcher m = pattern.matcher(code);
            while (m.find()&&!m.group(1).contains("throw")&&!m.group(1).contains("new")) {//排除关键字干扰
                FunParams funParams = new FunParams();
                funParams.setFunction(i);
                if (!StringUtils.isEmpty(m.group(2).trim())&&m.group(2).split(" ").length>1)//参数列表不为空并且不是形如F(a,b)这样的调用构造函数
                {
                    String []params=m.group(2).trim().replace("\n", "").split(",");
                    funParams.setParams(params);
                } else {//参数列表为空
                    String empty[] = {};
                    funParams.setParams(empty);
                }
                list.add(funParams);
            }
        }
        //提取常规方法
        Matcher m =CPP_PATTERN.matcher(code);

        while (m.find()) {
            String fun=m.group(6);
            //排除关键字干扰
            if (!classlist.contains(fun) && !fun.equals("main") && !fun.contains("throw")
                    && !m.group(2).equals("new") && !m.group(2).equals("return") && !fun.equals("if")
                    &&!m.group(2).contains("throw")&&!fun.contains("this")&&!fun.equals("while")
                    &&!fun.equals("super")&&!fun.equals("for")&&!fun.equals("sizeof")
                    &&!fun.equals("void")&&!m.group(2).equals("typedef") &&!fun.equals("defined")
                    &&!fun.equals("free")) {
                FunParams funParams = new FunParams();
                //此处与Ｃ语言类似
                if (!StringUtils.isEmpty(m.group(7).trim())){
                    boolean flag=true;
                    String []params=m.group(7).trim().replace("\n", "").split(",");
                    for(int i=0;i<params.length;i++)
                    {
                        if(params!=null&&params.length==1&&params[0].contains("void"))
                            break;
                        if(params[i]==null||params[i].split(" ").length==1)
                        {
                            flag=false;
                            break;
                        }
                    }
                    if(flag==true)
                    {
                        funParams.setFunction(fun);
                        funParams.setParams(params);
                    }
                }
                else {
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
