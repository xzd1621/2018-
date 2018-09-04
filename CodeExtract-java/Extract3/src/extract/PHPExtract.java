package extract;

import bean.FunParams;
import org.apache.commons.lang.StringUtils;

import java.util.ArrayList;
import java.util.List;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

/**
 * PHP的函数提取较c,c++,java简单得多，
 * 所有函数都是function 函数名 参数列表　的形式
 * 提取正确率很高
 */
public class PHPExtract {

    public static Pattern PHP_PATTERN = Pattern.compile("function\\s+(.*?)\\((.*?\\s*.*?)\\)\\s*");

    /**
     * php提取函数参数
     *
     * @param code
     * @return
     */
    public static List<FunParams> extractfunction(String code) {
        Matcher m = PHP_PATTERN.matcher(code);
        ArrayList<FunParams> list = new ArrayList<FunParams>();
        while (m.find()) {
            FunParams funParams = new FunParams();
            funParams.setFunction(m.group(1));
            if (!StringUtils.isEmpty(m.group(2).trim())) {
                funParams.setParams(m.group(2).trim().replace("\n", "").split(","));
            } else {
                String empty[] = {};
                funParams.setParams(empty);
            }
            list.add(funParams);
        }
        return list;
    }

}
