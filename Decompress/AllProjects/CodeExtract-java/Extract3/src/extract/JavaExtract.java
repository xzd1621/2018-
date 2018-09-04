package extract;

import bean.FunParams;
import org.apache.commons.lang.StringUtils;

import java.util.ArrayList;
import java.util.List;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

/**
 * 提取java的与提取c++的完全相同，二者语法比较类似
 * 可以兼容c++,java
 */

public class JavaExtract {

    public static Pattern JAVA_CLASS_PATTERN = Pattern.compile("class\\s+(\\w+).*\\s*(:|\\{|extends|implements)");

    public static Pattern JAVA_PATTERN = Pattern.compile("((\\w+<*\\w*>*\\[*]*\\w*)((\\s+[\\*&]*\\s*)|(\\s*[\\*&]*\\s+))(\\w+)\\s*\\((.*?\\s*.*?\\s*.*?)\\s*\\))");

    /**
     * 提取类名(java   cpp需要)
     *
     * @param code
     * 80 files 20seconds
     */
    public static List<String> extractclass(String code) {
        ArrayList<String> classlist = new ArrayList<String>();
        Matcher m = JAVA_CLASS_PATTERN.matcher(code);
        while (m.find()) {
            classlist.add(m.group(1).trim().replace("\n", ""));
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
            Pattern pattern = Pattern.compile("(.*?)\\s+" + i + "\\s*\\((.*?\\s*.*?\\s*.*?)\\)\\s*");
            Matcher m = pattern.matcher(code);
            while (m.find()&&!m.group(1).contains("throw")&&!m.group(1).contains("new")) {
                FunParams funParams = new FunParams();
                funParams.setFunction(i);
                if (!StringUtils.isEmpty(m.group(2).trim())&&m.group(2).split(" ").length>1)
                {
                    String []params=m.group(2).trim().replace("\n", "").split(",");
                    funParams.setParams(params);
                } else {
                    String empty[] = {};
                    funParams.setParams(empty);
                }
                list.add(funParams);
            }
        }
        //提取常规方法
        Matcher m = JAVA_PATTERN.matcher(code);

        while (m.find()) {
            String fun=m.group(6);
            if (!classlist.contains(fun) && !fun.equals("main") && !fun.contains("throw")
                    && !m.group(2).equals("new") && !m.group(2).equals("return") && !fun.equals("if")
                    &&!m.group(2).contains("throw")&&!fun.contains("this")&&!fun.equals("while")
                    &&!fun.equals("super")&&!fun.equals("for")&&!fun.equals("sizeof")
                    &&!fun.equals("void")&&!m.group(2).equals("typedef") &&!fun.equals("defined")
                    &&!fun.equals("free")) {
                FunParams funParams = new FunParams();
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
