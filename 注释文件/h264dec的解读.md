==================================================================================================================
class MultiFileWriter:

这段代码定义了一个名为`MultiFileWriter`的类，它继承自`CompressedWriter`类。`MultiFileWriter`的主要功能是将压缩数据（如H.264编码的视频流）写入一个或多个文件。

类成员变量：

- `filename`：表示文件名的字符串。

构造函数：

- `MultiFileWriter(std::string fname)`：使用传入的文件名字符串`fname`初始化`filename`成员变量。

成员函数：

- `Write(int streamId, const uint8_t*data, unsigned int size)`：根据`streamId`将指定大小的`data`（一段压缩数据，如H.264编码的视频流）写入一个文件。如果`streamId`不等于`CompressionStream::DEFAULT_STREAM`，则将`streamId`附加到文件名后。该函数使用`fopen`，`fwrite`和`fclose`函数将数据写入文件，并在成功时返回写入的数据大小和`WelsDec::ERR_NONE`，在写入失败时返回0和`WelsDec::ERR_BOUND`。
  
- `Close()`：虚拟函数，用于关闭文件。在此实现中，不执行任何操作，因为文件在`Write`函数中已经关闭。

`MultiFileWriter`类的主要用途是将压缩数据（如H.264编码的视频流）写入一个或多个文件，这些文件可以是分离的视频流，以便稍后进行解码和播放。

==================================================================================================================
class FlushOnClose:

这段代码定义了一个名为`FlushOnClose`的类。该类的主要目的是在其析构函数中将压缩数据（如H.264编码的视频流）写入一个或多个文件。该类使用了前面提到的`MultiFileWriter`类。

类成员变量：

- `filename`：表示文件名的字符串。

构造函数：

- `FlushOnClose(std::string fname)`：使用传入的文件名字符串`fname`初始化`filename`成员变量。

成员函数：

- `nop()`：一个无操作（No Operation）函数，可能用于在某些情况下防止编译器优化。

析构函数：

- `~FlushOnClose()`：在析构时执行以下操作：
  1. 创建一个`MultiFileWriter`对象`mfw`，并传入`filename`。
  2. 如果`oMovie().isRecoding`为`true`，则调用`iMovie().setOriginalFileSize(oMovie().def().len())`以设置原始文件大小。
  3. 使用`oMovie().flushToWriter(mfw)`将压缩数据（如H.264编码的视频流）写入一个或多个文件。
  4. 调用`mfw.Close()`关闭文件。

`FlushOnClose`类在析构时利用`MultiFileWriter`类将压缩数据（如H.264编码的视频流）写入文件。这样，在`FlushOnClose`类的对象离开其作用域时，数据将被自动写入文件并关闭。这是一种利用RAII（Resource Acquisition Is Initialization）技术在C++中自动管理资源的方法。
==================================================================================================================
void H264DecodeInstance (ISVCDecoder* pDecoder, const char* kpH264FileName, const char* kpOuputFileName, const char * yuvFileName,
                         int32_t& iWidth, int32_t& iHeight, const char* pOptionFileName, const char* pLengthFileName):


version1:
这段代码定义了一个名为 `H264DecodeInstance` 的函数，它负责解码 H.264 格式的输入文件，并将解码后的数据保存到输出文件中。函数使用了前面提到的 `FlushOnClose` 类和 `MultiFileWriter` 类。

函数参数：

- `ISVCDecoder* pDecoder`：解码器接口指针，用于解码 H.264 数据。
- `const char* kpH264FileName`：输入 H.264 文件名。
- `const char* kpOuputFileName`：输出文件名。
- `const char* yuvFileName`：YUV 格式文件名，用于保存解码后的数据。
- `int32_t& iWidth`：输出视频宽度的引用。
- `int32_t& iHeight`：输出视频高度的引用。
- `const char* pOptionFileName`：可选文件名，用于保存额外信息。
- `const char* pLengthFileName`：长度文件名，用于读取切片大小。

函数主要执行以下操作：

1. 打开和准备输入、输出文件，包括 H.264 文件、YUV 文件、可选文件和长度文件。
2. 使用 `FlushOnClose` 类创建一个对象 `foc`，用于在函数退出时自动保存输出文件。
3. 初始化相关变量，如时间戳、文件大小、缓冲区等。
4. 循环读取 H.264 文件中的切片，根据切片大小进行解码，并将解码后的数据保存到 YUV 文件。
5. 在解码过程中，记录解码的宽度、高度、帧数等信息。
6. 在循环结束后，输出解码统计信息，如宽度、高度、帧数、解码时间、帧率等。
7. 使用 `foc.nop()` 确保析构函数被调用。
8. 关闭所有打开的文件，并释放内存。

这个函数的主要任务是读取 H.264 格式的视频文件，然后使用 `ISVCDecoder` 接口进行解码，并将解码后的数据写入 YUV 格式的输出文件。在这个过程中，还可以通过可选文件和长度文件来进行额外的配置。



version2：
这段代码定义了一个名为`H264DecodeInstance`的函数，它负责解码H.264视频文件并将解码后的数据写入一个YUV文件。该函数接收一系列参数，包括解码器对象、输入文件名、输出文件名等，然后逐帧解码输入文件并将结果写入输出文件。

函数参数：

- `ISVCDecoder* pDecoder`：解码器对象指针。
- `const char* kpH264FileName`：输入H.264视频文件名。
- `const char* kpOuputFileName`：输出文件名。
- `const char* yuvFileName`：输出YUV文件名。
- `int32_t& iWidth`：解码后的视频宽度。
- `int32_t& iHeight`：解码后的视频高度。
- `const char* pOptionFileName`：用于存储输出视频分辨率改变的附加文件名。
- `const char* pLengthFileName`：用于存储每个NALU长度的文件名。

函数流程：

1. 初始化文件指针和其他所需变量。
2. 创建一个`FlushOnClose`类的对象`foc`，用于将解码数据写入文件。
3. 根据输入和输出文件名，判断是录制还是解码模式，并执行相应的初始化操作。
4. 打开输入和输出文件，并进行相关的错误检查。
5. 设置解码器选项，如数据格式。
6. 读取输入文件并存储到缓冲区`pBuf`。
7. 循环处理输入缓冲区的每一帧数据：
    - 读取当前帧的长度。
    - 调用解码器的解码函数。
    - 如果解码成功，将解码后的数据处理并写入YUV文件，同时更新宽度和高度等信息。
    - 移动缓冲区位置，准备读取下一帧。
8. 输出解码过程的统计信息。
9. 清理资源，关闭文件指针，并调用`foc.nop()`。

该函数的主要作用是使用给定的解码器对象逐帧解码H.264文件，并将解码后的数据写入指定的YUV文件。在解码过程中，会输出一些统计信息，如宽度、高度、帧数、解码时间等。最后，函数会自动释放所占用的资源。