package extract;

import bean.FunParams;
import net.sf.json.JSONArray;
import net.sf.json.JSONObject;

import java.util.ArrayList;
import java.util.List;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

public class Main {
    //将函数的参数列表转化为json格式输出
    public void printjson(List<FunParams> functiondict)
    {
        JSONArray func=new JSONArray();
        func.clear();
        for (FunParams i:functiondict
        ) {
            JSONObject temp=new JSONObject();
            JSONArray arr=new JSONArray();
            temp.put("func",i.getFunction());
            if (i.getParams()!=null)
            for (String j:i.getParams()
            ) {
                arr.add(j);
            }
            temp.put("params",arr);
            func.add(temp);
        }

    }
    //输出类的名字
    public void printclass(List<String> classlist)
    {
        for (String clist:classlist
             ) {
            System.out.println(clist);
        }
    }
    /**
     *预处理时将代码里的所有注释去掉，避免注释的干扰
     * 注释有/**……* /,//,#这几种
     * 正则匹配注释，替换为空
     */
    public String replacenotes(String code) {
        Pattern pattern=Pattern.compile("(\\/\\/.*)|(/\\*+[\\s\\S]*?\\*+/)|(#.*)");
        Matcher m=pattern.matcher(code);
        while(m.find())
        {
            if (m.group(1)!=null)
            {
                code= code.replace(m.group(1),"");

            }
            if (m.group(2)!=null)
            {
                code= code.replace(m.group(2),"");
            }
            if (m.group(3)!=null)
            {
                code= code.replace(m.group(3),"");
            }
        }
        return code;
    }

    public static void main(String []args)
    {
        System.out.println("Hello,World!");

        FileExtract fileExtract = new FileExtract();
        fileExtract.ReadFile("/home/xu/document/code/php");
        CExtract cex = new CExtract();
        CppExtract cppex=new CppExtract();
        JavaExtract javaex=new JavaExtract();
        PHPExtract phpex=new PHPExtract();
        Main main=new Main();

        for (int i = 0; i < fileExtract.codelist.size(); i++)
        {
            System.out.println("\n"+i);
            String code=fileExtract.codelist.get(i);
            code=main.replacenotes(code);
            String filename=fileExtract.filenamelist.get(i);
            System.out.println(filename);
            System.out.println("MD5: "+fileExtract.getMD5(code.getBytes()));
            String suffix = filename.substring(filename.lastIndexOf(".") + 1);//get the houzhui
            System.out.println(suffix);
            /**
             * 根据文件类型调用相应的处理函数
             */
            if (suffix.equals("c")||suffix.equals("pc"))
            {
                main.printjson(cex.extractfunction(code));
            }
            else if (suffix.equals("cpp")||suffix.equals("cc")||suffix.equals("h")||suffix.equals("hh")
                    ||suffix.equals("hpp")||suffix.equals("cxx")||suffix.equals("hxx")||suffix.equals("inl")||
                    suffix.equals("ipp"))
            {
                main.printclass(cppex.extractclass(code));
                main.printjson(cppex.extractfunction(code));
            }
            else if (suffix.equals("java"))
            {
                main.printclass(javaex.extractclass(code));
                main.printjson(javaex.extractfunction(code));
            }
            else if (filename.contains(".php"))
            {
                main.printjson(phpex.extractfunction(code));
            }
        }
    }
}
