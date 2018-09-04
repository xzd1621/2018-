package extract;

import java.io.*;
import java.security.MessageDigest;
import java.security.NoSuchAlgorithmException;
import java.util.ArrayList;

public class FileExtract {
    public ArrayList<String> codelist=new ArrayList <String>();
    protected ArrayList <String> filenamelist=new ArrayList <String>();

    /**
     * 对文件的一些操作
     * 包括文件的读取，md5值的获取
     * @param fileName
     * @return
     */
    public String readToString(String fileName) {//filname 是文件路径/文件名的形式，读取文件，将一整个文件转化为字符串
        String encoding = "utf-8";
        File file = new File(fileName);
        Long filelength = file.length();
        byte[] filecontent = new byte[filelength.intValue()];
        try {
            FileInputStream in = new FileInputStream(file);
            in.read(filecontent);
            in.close();
        } catch (FileNotFoundException e) {
            e.printStackTrace();
        } catch (IOException e) {
            e.printStackTrace();
        }
        try {
            return new String(filecontent, encoding);
        } catch (UnsupportedEncodingException e) {
            System.err.println("The OS does not support " + encoding);
            e.printStackTrace();
            return null;
        }
    }

    //传入文件所在的文件夹路径，得到文件夹里的文件组成的文件名列表和文件字符串列表
    public void ReadFile(String path)
    {
        File file=new File(path);
        File []filelist=file.listFiles();
        for (int i=0;i<filelist.length;i++)
        {
            if(filelist[i].isFile())
            {
                System.out.println("file: "+filelist[i].toString());
                filenamelist.add(filelist[i].toString().replace(path+"/",""));
                codelist.add(readToString(filelist[i].toString()));
            }
        }
    }

    //get the md5 of the code
    public static String getMD5(byte[] source) {
        String s = null;
        char hexDigits[] = { '0', '1', '2', '3', '4', '5', '6', '7', '8', '9',
                'a', 'b', 'c', 'd', 'e', 'f' };// 用来将字节转换成16进制表示的字符
        try {
            MessageDigest md = MessageDigest
                    .getInstance("MD5");
            md.update(source);
            byte tmp[] = md.digest();// MD5 的计算结果是一个 128 位的长整数，
            // 用字节表示就是 16 个字节
            char str[] = new char[16 * 2];// 每个字节用 16 进制表示的话，使用两个字符， 所以表示成 16
            // 进制需要 32 个字符
            int k = 0;// 表示转换结果中对应的字符位置
            for (int i = 0; i < 16; i++) {// 从第一个字节开始，对 MD5 的每一个字节// 转换成 16
                // 进制字符的转换
                byte byte0 = tmp[i];// 取第 i 个字节
                str[k++] = hexDigits[byte0 >>> 4 & 0xf];// 取字节中高 4 位的数字转换,// >>>
                // 为逻辑右移，将符号位一起右移
                str[k++] = hexDigits[byte0 & 0xf];// 取字节中低 4 位的数字转换

            }
            s = new String(str);// 换后的结果转换为字符串

        } catch (NoSuchAlgorithmException e) {
            e.printStackTrace();
        }
        return s;
    }

}
