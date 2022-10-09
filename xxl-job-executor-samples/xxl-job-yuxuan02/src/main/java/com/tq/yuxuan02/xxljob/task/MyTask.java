package com.tq.yuxuan02.xxljob.task;

import com.xxl.job.core.context.XxlJobHelper;
import com.xxl.job.core.handler.annotation.XxlJob;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.stereotype.Component;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;

@Component
public class MyTask {

    private static Logger logger = LoggerFactory.getLogger(MyTask.class);

    @XxlJob("bar_strategy_backtest")
    public void demoJobHandler() throws Exception {
        // 在管理平台上打印
        XxlJobHelper.log("TransQuant bar回测任务启动.");
        // 在控制台上打印
        logger.info("Backtest Service Starting.....");
        Process proc;
        try {
            proc = Runtime.getRuntime().exec("python /Users/xuan/Documents/transmatrix/bar_strategy.py");
            BufferedReader in = new BufferedReader(new InputStreamReader(proc.getInputStream()));
            String line = null;
            while ((line = in.readLine()) != null) {
                System.out.println(line);
                XxlJobHelper.log(line);
            }
            in.close();
            proc.waitFor();
        } catch (IOException e) {
            e.printStackTrace();
        } catch (InterruptedException e) {
            e.printStackTrace();
        }
        XxlJobHelper.log("TransQuant bar回测任务完成.");
    }
}
