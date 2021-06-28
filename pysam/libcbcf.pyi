import sys
from typing import (
    Optional,
    Union,
    Any,
    Sequence,
    Tuple,
    Iterator,
    List,
    Iterable,
    Dict,
    overload,
    TypeVar,
    Mapping, Generic,
)

if sys.version_info < (3, 8):
    from typing_extensions import Literal
else:
    from typing import Literal

from .libchtslib import HTSFile, _HasFileNo

_D = TypeVar("_D")
_K = TypeVar("_K", str, Union[int, str])
_V = TypeVar("_V")

class _Mapping(Generic[_K, _V]):
    def __len__(self) -> int: ...
    def __contains__(self, key: _K) -> bool: ...
    def __iter__(self) -> str: ...
    def iterkeys(self) -> Iterator[str]: ...
    def itervalues(self) -> Iterator[_V]: ...
    def iteritems(self) -> Iterator[Tuple[str, _V]]: ...
    def keys(self) -> List[str]: ...
    def items(self) -> List[Tuple[str, _V]]: ...
    def values(self) -> List[_V]: ...
    def __bool__(self) -> bool: ...
    def __getitem__(self, key: _K) -> _V: ...
    def get(self, key: _K, default: _D = ...) -> Union[_D, _V]: ...

class VariantHeaderRecord(_Mapping[str, str]):
    @property
    def header(self) -> VariantHeader: ...
    @property
    def type(self) -> Optional[str]: ...
    @property
    def key(self) -> Optional[str]: ...
    @property
    def value(self) -> Optional[str]: ...
    @property
    def attrs(self) -> Sequence[Tuple[str, str]]: ...
    def update(self, items: Union[Iterable, Dict] = ..., **kwargs) -> None: ...
    def pop(self, key: str, default: str = ...) -> str: ...
    def remove(self) -> None: ...  # crashes

class VariantHeaderRecords:
    @property
    def header(self) -> VariantHeader: ...
    def __len__(self) -> int: ...
    def __bool__(self) -> bool: ...
    def __getitem__(self, index) -> VariantHeaderRecord: ...
    def __iter__(self) -> Iterator[VariantHeaderRecord]: ...

class VariantMetadata:
    @property
    def header(self) -> VariantHeader: ...
    @property
    def name(self) -> str: ...
    # @property  # should this be exposed?
    # def id(self) -> int: ...
    @property
    def number(self) -> Optional[str]: ...
    @property
    def type(self) -> Optional[str]: ...
    @property
    def description(self) -> Optional[str]: ...
    @property
    def record(self) -> Optional[VariantHeaderRecord]: ...
    def remove_header(self) -> None: ...

class VariantHeaderMetadata(_Mapping[str, VariantMetadata]):
    @property
    def header(self) -> VariantHeader: ...
    def add(
        self,
        id: str,
        number: Optional[str],
        type: Optional[str],
        description: str,
        **kwargs
    ) -> None: ...
    def remove_header(self, key: str) -> None: ...
    def clear_header(self) -> None: ...

class VariantContig:
    @property
    def header(self) -> VariantHeader: ...
    @property
    def name(self) -> str: ...
    @property
    def id(self) -> int: ...
    @property
    def length(self) -> Optional[int]: ...
    @property
    def header_record(self) -> VariantHeaderRecord: ...
    def remove_header(self) -> None: ...

class VariantHeaderContigs(_Mapping[Union[int, str], VariantContig]):
    @property
    def header(self) -> VariantHeader: ...
    def remove_header(self, key: Union[int, str]) -> None: ...
    def clear_header(self) -> None: ...
    def add(self, id: str, length: Optional[int] = ..., **kwargs) -> None: ...

class VariantHeaderSamples:
    @property
    def header(self) -> VariantHeader: ...
    def __len__(self) -> int: ...
    def __bool__(self) -> bool: ...
    def __getitem__(self, index: str) -> str: ...
    def __iter__(self) -> Iterator[str]: ...
    def __contains__(self, key: str) -> bool: ...
    def add(self, name: str) -> None: ...

class VariantHeader:
    def __init__(self) -> None: ...
    def __bool__(self) -> bool: ...
    def copy(self) -> VariantHeader: ...
    def merge(self, header: VariantHeader) -> None: ...
    @property
    def version(self) -> str: ...
    @property
    def samples(self) -> VariantHeaderSamples: ...
    @property
    def records(self) -> VariantHeaderRecords: ...
    @property
    def contigs(self) -> VariantHeaderContigs: ...
    @property
    def filters(self) -> VariantHeaderMetadata: ...
    @property
    def info(self) -> VariantHeaderMetadata: ...
    @property
    def formats(self) -> VariantHeaderMetadata: ...
    @property
    def alts(self) -> Dict[str, VariantHeaderRecord]: ...
    def new_record(
        self,
        contig: Optional[str] = ...,
        start: int = ...,
        stop: int = ...,
        alleles: Optional[Tuple[str]] = ...,
        id: Optional[str] = ...,
        qual: Optional[int] = ...,
        filter: Optional[Any] = ...,
        info: Optional[Mapping[str, _InfoValue]] = ...,
        samples: Optional[Iterable[str]] = ...,
        **kwargs
    ) -> VariantRecord: ...
    def add_record(self, record: VariantHeaderRecord) -> None: ...
    def add_line(self, line: str) -> None: ...
    @overload
    def add_meta(
        self, key: str, value: None = ..., items: Iterable[Tuple[str, str]] = ...
    ) -> None: ...
    @overload
    def add_meta(self, key: str, value: str = ..., items: None = ...) -> None: ...
    def add_sample(self, name: str) -> None: ...

class VariantRecordFilter(_Mapping[Union[int, str],VariantMetadata]):
    def add(self, key: str) -> None: ...
    def __delitem__(self, key: Union[int, str]) -> None: ...
    def clear(self) -> None: ...
    def __eq__(self, other) -> bool: ...
    def __ne__(self, other) -> bool: ...

class VariantRecordFormat(_Mapping[str, VariantMetadata]):
    def __delitem__(self, key: str) -> None: ...
    def clear(self) -> None: ...

_InfoValue = Any  # TODO see bcf_info_get_value

class VariantRecordInfo(_Mapping[str, _InfoValue]):
    def __setitem__(self, key: str, object: _InfoValue) -> None: ...
    def __delitem__(self, key: str) -> None: ...
    def clear(self) -> None: ...
    def update(
        self, items: Optional[Mapping[str, _InfoValue]] = ..., **kwargs
    ) -> None: ...
    def pop(self, key: str, default: _D = ...) -> Union[_D, _InfoValue]: ...
    def __eq__(self, other) -> bool: ...
    def __ne__(self, other) -> bool: ...

class VariantRecordSamples(_Mapping[str, "VariantRecordSample"]):
    def __eq__(self, other) -> bool: ...
    def __ne__(self, other) -> bool: ...
    # TODO Do these work? Isn’t the container read only?
    def update(
        self, items: Optional[Mapping[str, VariantRecordSample]] = ..., **kwargs
    ) -> None: ...
    def pop(self, key: str, default: _D = ...) -> Union[_D, VariantRecordSample]: ...

class VariantRecord:
    @property
    def header(self) -> VariantHeader: ...
    def copy(self) -> VariantRecord: ...
    def translate(self, dst_header: VariantHeader) -> None: ...
    rid: int
    chrom: str
    contig: str
    pos: int
    start: int
    stop: int
    rlen: int
    qual: Optional[int]
    id: Optional[str]
    ref: Optional[str]
    alleles: Optional[Tuple[str]]
    alts: Optional[Tuple[str]]
    @property
    def filter(self) -> VariantRecordFilter: ...
    @property
    def info(self) -> VariantRecordInfo: ...
    @property
    def format(self) -> VariantRecordFormat: ...
    @property
    def samples(self) -> VariantRecordSamples: ...
    def __eq__(self, other) -> bool: ...
    def __ne__(self, other) -> bool: ...

_FormatValue = Any  # TODO see bcf_format_get_value

class VariantRecordSample(_Mapping[str, _FormatValue]):
    @property
    def index(self) -> int: ...
    @property
    def name(self) -> str: ...
    allele_indices: Optional[Tuple[Optional[int]]]
    alleles: Optional[Tuple[Optional[str]]]
    phased: bool
    def __setitem__(self, key: str, value: _FormatValue) -> None: ...
    def __delitem__(self, key: str) -> None: ...
    def clear(self) -> None: ...
    def update(
        self, items: Optional[Mapping[str, _FormatValue]] = ..., **kwargs
    ) -> None: ...
    def pop(self, key: str, default: _D = ...) -> Union[_D, _FormatValue]: ...
    def __eq__(self, other) -> Any: ...
    def __ne__(self, other) -> Any: ...

class BaseIndex(_Mapping[Union[int, str], str]):
    refs: Sequence[str]
    refmap: Dict[str, str]
    def __init__(self) -> None: ...
    # TODO Do these work? Isn’t the container read only?
    def update(self, items: Optional[Mapping[str, str]] = ..., **kwargs) -> None: ...
    def pop(self, key: str, default: _D = ...) -> Union[_D, str]: ...

class BCFIndex(BaseIndex):
    @property
    def header(self) -> VariantHeader: ...
    def __init__(self) -> None: ...
    def fetch(
        self,
        bcf: VariantFile,
        contig: str,
        start: Optional[int],
        stop: Optional[int],
        reopen: bool,
    ) -> BCFIterator: ...

class TabixIndex(BaseIndex):
    def __init__(self) -> None: ...
    def fetch(
        self,
        bcf: VariantFile,
        contig: str,
        start: Optional[int],
        stop: Optional[int],
        reopen: bool,
    ) -> TabixIterator: ...

class BaseIterator:
    def __init__(self) -> None: ...

class BCFIterator(BaseIterator):
    def __init__(
        self,
        bcf: VariantFile,
        contig: str,
        start: Optional[int] = ...,
        stop: Optional[int] = ...,
        reopen: bool = ...,
    ) -> None: ...
    def __iter__(self) -> BCFIterator: ...
    def __next__(self) -> VariantRecord: ...

class TabixIterator(BaseIterator):
    def __init__(
        self,
        bcf: VariantFile,
        contig: str,
        start: Optional[int] = ...,
        stop: Optional[int] = ...,
        reopen: bool = ...,
    ) -> None: ...
    def __iter__(self) -> TabixIterator: ...
    def __next__(self) -> VariantRecord: ...

class VariantFile(HTSFile):
    @property
    def header(self) -> VariantHeader: ...
    @property
    def index(self) -> BaseIndex: ...
    @property
    def drop_samples(self) -> bool: ...
    @property
    def is_reading(self) -> bool: ...
    @property
    def header_written(self) -> bool: ...
    def __init__(
        self,
        filename: Union[str, bytes, int, _HasFileNo],
        mode: Optional[Literal["r", "w", "wh", "rb", "wb", "wbu", "wb0"]] = ...,
        index_filename: Optional[str] = ...,
        header: Optional[VariantHeader] = ...,
        drop_samples: bool = ...,
        duplicate_filehandle: bool = ...,
        ignore_truncation: bool = ...,
        threads: int = ...,
    ) -> None: ...
    def close(self) -> None: ...
    def __iter__(self) -> VariantFile: ...
    def __next__(self) -> VariantRecord: ...
    def copy(self) -> VariantFile: ...
    def open(
        self,
        filename: Union[str, bytes, int, _HasFileNo],
        mode: Optional[Literal["r", "w", "wh", "rb", "wb", "wbu", "wb0"]] = ...,
        index_filename: Optional[str] = ...,
        header: Optional[VariantHeader] = ...,
        drop_samples: bool = ...,
        duplicate_filehandle: bool = ...,
        ignore_truncation: bool = ...,
        threads: int = ...,
    ) -> None: ...
    def reset(self) -> None: ...
    def is_valid_tid(self, tid: int) -> bool: ...
    def get_tid(self, reference: str) -> int: ...
    def get_reference_name(self, tid: int) -> str: ...
    def fetch(
        self,
        contig: Optional[str] = ...,
        start: Optional[int] = ...,
        stop: Optional[int] = ...,
        region: Optional[str] = ...,
        reopen: bool = ...,
        end: Optional[int] = ...,
        reference: Optional[str] = ...,
    ) -> Iterator[VariantRecord]: ...
    def new_record(self, *args, **kwargs) -> Any: ...
    def write(self, record: VariantRecord) -> int: ...
    def subset_samples(self, include_samples: Iterable[str]) -> None: ...
