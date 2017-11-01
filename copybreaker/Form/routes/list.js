var express = require('express');
var router = express.Router();
var multer = require('multer');
var mysql = require('mysql');
var fs = require('fs');
var pool = mysql.createPool({
  connectionLimit: 5,
  host: 'localhost',
  user:'root',
  database:'copybreaker',
  password:'bojima7306'
});
var multer=require('multer');

var storage = multer.diskStorage({
  destination: function (req, file, cb) {
    cb(null, 'uploads/') // cb 콜백함수를 통해 전송된 파일 저장 디렉토리 설정
  },
  filename: function (req, file, cb) {
    cb(null, file.originalname) // cb 콜백함수를 통해 전송된 파일 이름 설정
  }
});
var upload = multer({ storage: storage });
var multipart = require('connect-multiparty');
var multipartMiddleware = multipart();

const shelljs = require('shelljs');

/* GET home page. */
router.get('/', function(req, res, next) {
  pool.getConnection(function(err,connection){
    var sqlForSelectList = "SELECT idx, date, title FROM board ";
    connection.query(sqlForSelectList, function(err,rows){
      if (err) console.err("err : " + err );
      console.log("rows : " + JSON.stringify(rows));

      res.render('list',{title: 'copybreaker', rows:rows});
      connection.release();
    });
  });
});

//파일업로드 로직 처리 GET
router.get('/fileupload', function(req, res, next){
  res.render('fileupload');
});

//파일업로드 로직 처리 POST
router.post('/fileupload',upload.single('title'), function(req, res, next){
   
   var title =  req.file.originalname;
   var title1 = req.body.title;
   var datas = [title];
 
   console.log(req.body);
   pool.getConnection(function (err, connection)
   {

      //Use the connection
       var sqlForInsertBoard = "insert into board(title) values(?)";

      connection.query(sqlForInsertBoard, datas, function(err, rows) {
         console.log("rows: " + JSON.stringify(rows));
       

         res.redirect('/list');
         connection.release();

         //Don't use the connection here, it has been returned to the pool.
      });
   });

});

// 삭제 로직 처리 GET
router.get('/delete/:idx', function(req, res, next){
   var idx = req.params.idx;

    pool.getConnection(function(err, connection)
    {
       var sql = "select idx, date, title from board where idx=?";
        //sql += "";
        var val = ";update board set hit = hit + 1 where idx=?"
        connection.query(sql,[idx], function(err,rows)
        {
            if(err) console.error(err);
            console.log("삭제 목록 확인 : ",rows);
            res.render('delete', {title:"문서 삭제", row:rows[0]});
            connection.release();
        });
    });
});

// 삭제 로직 처리 POST
router.post('/delete', function(req,res,next)
{
    var idx = req.body.idx;
    var title= 'uploads/'+req.body.title;

    pool.getConnection(function(err, connection)
    {

      var sql = "delete from board where idx=?";
      connection.query(sql, [idx], function(err,result)
      {
          console.log(result);
          if(err) console.error("삭제 중 에러 발생 err : ",err);

          fs.unlink(title);
          res.redirect('/list');
          
          connection.release();
      });
    });
});


///////////////////////////////////////////////// 결과화면 /////////////////////////////////////////////////

router.get('/result1', function(req, res, next){    
   res.render('result1',{title: '1 : 1 Similarity Check'});             
});

router.post('/result1', function(req, res, next){
   var title1 = req.body.title1;
   var title2 = req.body.title2;

   shelljs.exec('python3 ~/Desktop/copybreaker/Form/views/test/project.py' + " " + title1 + " " + title2, function (code, stdout, stderr){
   console.log("Exit code : ", code);
   console.log("Output : ", stdout);
   console.log("StdErr : ", stderr);
   console.log("-------------------------------------");

   res.redirect('/list');
   //res.render('result1');
   });
});

router.get('/result2', function(req, res, next){
    res.render('result2');
});

router.post('/result2', function(req, res, next){
   var titles = req.body.title;
   var t;
   for(var i=0 ; i<titles.length ; i++){
      t += titles[i] + " "
   }
   shelljs.exec('python3 ~/Desktop/copybreaker/Form/views/test2/project2.py' + " " + t, function (code, stdout, stderr){
   console.log("Exit code : ", code);
   console.log("Output : ", stdout);
   console.log("StdErr : ", stderr);
   console.log("-------------------------------------");

   res.redirect('/list');
   //res.render('result2');
   });
});

//////////////////////////////////////////////////////////////////////////////////////////////////

module.exports = router;

